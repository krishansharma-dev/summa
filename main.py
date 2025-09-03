
from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
def main():
    return {"welcome": "to FastAPI"}

@app.get("/post")
def read_post():
    return {"post": "This is a post"}

@app.post("/createpost")
def create_post( payload: dict = Body(...) ):
    print(payload)
    return {"title": payload['title'], "content": payload['content']
            ,"author": payload['author'] ,
            "tags": payload['tags'] ,
            }