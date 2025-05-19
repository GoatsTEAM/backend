from fastapi import FastAPI
from uvicorn import run

from app.api.v1.metrics import router as api_router
from app.db import init_mongo
from app.dependencies.services_factory import get_services_factory
from app.events.router import Router
from app.kafka import get_kafka


services = get_services_factory()
event_router = Router(services)

app = FastAPI()
app.include_router(api_router)


async def main():
    run(
        "app.main:app", reload=True, log_level="info", host="0.0.0.0", port=8000
    )
    await init_mongo()
    consumer, producer = get_kafka()
    async for request in consumer.events():
        response = await event_router.route(request)
        producer.produce(response)
