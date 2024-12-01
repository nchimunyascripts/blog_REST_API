"""Fast API"""
from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, schemas, utils
from .database import engine, get_db
from .router import post, user, auth

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


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    """HOME"""
    return {
        "message": "Hello World"
    }
