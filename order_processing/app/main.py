import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from uvicorn import run

from app.api.v1.cart import router as cart_router
from app.api.v1.order import router as order_router
from app.api.v1.delivery import router as delivery_router
from app.api.v1.metrics import router as metrics_router
from app.db import init_postgres
from app.dependencies.service_factory import get_services_factory
from app.events.consume_events import consume_events


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_postgres()
    services = get_services_factory()
    asyncio.create_task(consume_events(services))
    
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(cart_router)
app.include_router(order_router)
app.include_router(delivery_router)
app.include_router(metrics_router)


if __name__ == "__main__":
    run("app.main:app", reload=True, log_level="info", host="0.0.0.0", port=8000)