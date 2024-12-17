"""Fast API"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .router import post, user, auth, vote

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ['http://127.0.0.1:800/']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"]
)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    """HOME"""
    return {
        "message": "Hello World"
    }
