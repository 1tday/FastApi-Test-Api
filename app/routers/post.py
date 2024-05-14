from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=['Post']
)

@router.get("/",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),
              user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts ORDER BY id ASC""")
    # posts = cursor.fetchall() 
    posts = db.query(models.Post).all()
    return posts
router

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                  user_id: int = Depends(oauth2.get_current_user)):
    #cursor.execute(f"""INSERT INTO posts (title, content, published) 
    #               VALUES ({post.title}, {post.content}, {post.published})""")
    # так делать нельзя. база подвержена sql инъекциям.
    # cursor.execute("""INSERT INTO posts (title, content, published) 
    #                VALUES (%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # conn.commit()
    
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db),
             user_id: int = Depends(oauth2.get_current_user)): 
    # cursor.execute("""Select * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id {id} not found"}
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id), ))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    deleted_posts = db.query(models.Post).filter(models.Post.id == id)


  
    
    if deleted_posts.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    deleted_posts.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET 
    #                title = %s, content = %s, published = %s 
    #                WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
