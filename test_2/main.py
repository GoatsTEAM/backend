from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(root_path="/test_2", title="Test API")

Instrumentator().instrument(app).expose(app)

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/tester")
def read_test():
    return {"message": "Hello, Tiny!"}



@app.get("/dede")
def read_test():
    return {"message": "Hello, Tiny!"}

