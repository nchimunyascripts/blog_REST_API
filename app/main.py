"""Fast API"""
import time
from uuid import uuid4
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    """POST Schema"""
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "Other Stuff", "content": "Something to die for love", "published": True, "rating": None, "id": 1},
    {"title": "Summer Time 3", "content": "Something to die for love", "published": False, "rating": 3, "id": 5}
]

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='postgres', user='postgres',
                                    password='0977398719', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Connected to PSQL')
        break
    except Exception as error:
        print('Connection to database failed!\nError: ', error)
        time.sleep(2)

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


@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {
        "data": posts
    }


@app.post("/posts",  status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {
        "data": new_post
    }


@app.get('/posts/{_id}')
async def get_post(_id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(_id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {_id} was not found!')
    return {
        "Data": post
    }


@app.delete('/posts/{_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(_id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(_id)))
    deleted_post = cursor.fetchone()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {_id} does not exist')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{_id}')
async def update_post(_id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, (str(_id))))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {_id} does not exist')
    return {'data': updated_post}
