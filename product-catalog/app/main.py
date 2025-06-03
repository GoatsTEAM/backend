from fastapi import FastAPI
from .api.v1 import products, categories, reviews, orders, search, media
from prometheus_client import generate_latest
from starlette.responses import Response

app = FastAPI(title="Product Catalog Service")

app.include_router(products.router, prefix="/api/v1", tags=["products"])
app.include_router(categories.router, prefix="/api/v1", tags=["categories"])
app.include_router(reviews.router, prefix="/api/v1", tags=["reviews"])
app.include_router(orders.router, prefix="/api/v1", tags=["orders"])
app.include_router(search.router, prefix="/api/v1", tags=["search"])
app.include_router(media.router, prefix="/api/v1", tags=["media"])

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
