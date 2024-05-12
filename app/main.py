from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel

from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2. extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db

from.routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
            user='postgres', password='12345', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)
   

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}





