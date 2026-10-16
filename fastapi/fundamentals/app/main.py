from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello():
    return f" Welcome to FastAPI"


@app.post("/add")
def add(a: int, b: int):
    return a + b
