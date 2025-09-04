from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    author: str
    tags: list[str] = []
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    { "id": 1, "title": "First Post", "content": "This is the first post", "author": "Alice", "tags": ["intro", "welcome"], "published": True, "rating": 5 },
    { "id": 2, "title": "Second Post", "content": "This is the second post", "author": "Bob", "tags": ["update"], "published": False, "rating": None }
]       
  
def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post 
          
@app.get("/")
def main():
    return {"welcome": "to FastAPI"}

@app.get("/posts")
def read_post():
    return {"posts": my_posts}

@app.post("/posts")
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)   # ✅ add id here
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    print(post)
    return {"post_detail": post}
  