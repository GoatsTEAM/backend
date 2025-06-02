import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from uvicorn import run

from app.api.v1.metrics import router as api_router
from app.db import init_mongo
from app.dependencies.services_factory import get_services_factory
from app.events.consume_events import consume_events


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_mongo()
    services = get_services_factory()
    asyncio.create_task(consume_events(services))
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)


async def main():
    run("app.main:app", reload=True, log_level="info", host="0.0.0.0", port=8000)
