"""Fast API"""
from uuid import uuid4
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()





my_posts = [
    {"title": "Other Stuff", "content": "Something to die for love", "published": True, "rating": None, "id": 1},
    {"title": "Summer Time 3", "content": "Something to die for love", "published": False, "rating": 3, "id": 5}
]

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='postgres', user='postgres',
#                                     password='0977398719', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Connected to PSQL')
#         break
#     except Exception as error:
#         print('Connection to database failed!\nError: ', error)
#         time.sleep(2)


async def find_post(_id):
    for p in my_posts:
        if p['id'] == _id:
            return p


async def find_index_post(_id):
    for i, p in enumerate(my_posts):
        if p['id'] == _id:
            return i


@app.get("/")
async def root():
    """HOME"""
    return {
        "message": "Hello World"
    }


@app.get("/posts", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts",  status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get('/posts/{_id}', response_model=schemas.Post)
async def get_post(_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == _id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {_id} was not found!')
    return post


@app.delete('/posts/{_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(_id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == _id)
    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {_id} does not exist')
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{_id}', response_model=schemas.Post)
async def update_post(_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == _id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {_id} does not exist')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
