from app.db import init_mongo
from app.events.router import Router
from app.dependencies.services_factory import get_services_factory
from app.kafka import get_kafka


services = get_services_factory()
router = Router(services)


async def main():
    await init_mongo()
    consumer, producer = get_kafka()
    async for request in consumer.events():
        response = await router.route(request)
        producer.produce(response)
