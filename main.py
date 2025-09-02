
from fastapi import FastAPI

app = FastAPI()

@app.get("/login")
def main():
    return {"welcome": "to FastAPI"}

