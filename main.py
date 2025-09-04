from typing import Optional
from fastapi import FastAPI , Response , status , HTTPException
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

@app.post("/posts" , status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)   # ✅ add id here
    my_posts.append(post_dict)
    
    return {"data": post_dict}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[-1]
    return {"latest_post": post}       

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    return {"post_detail": post}

  
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = -1
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            index = i
            break
    
    if index == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )
    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT, detail=f"Post with id: {id} has been deleted" )
