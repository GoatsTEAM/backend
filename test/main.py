from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

Instrumentator().instrument(app).expose(app)

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}


def aaa():
    pass

def bbb():
    pass

@app.get("/tester")
def read_root():
    return {"message": "Hello, Tiny!"}