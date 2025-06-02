from app.events.router import Router
from app.kafka import get_kafka
from app.services import ServicesFactory
from app.events.handlers.reviews import reviews_router


async def consume_events(services: ServicesFactory):
    event_router = Router(services)
    event_router.include(reviews_router)
    consumer, producer = get_kafka()
    async for request in consumer.events():
        response = await event_router.route(request)
        producer.produce(response)
