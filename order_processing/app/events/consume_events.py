from app.events.router import Router
from app.kafka import get_kafka
from app.services import ServicesFactory
from app.events.handlers.cart import cart_router


async def consume_events(services: ServicesFactory):
    event_router = Router(services)
    event_router.include(cart_router)
    consumer, _ = get_kafka()
    async for request in consumer.events():
        await event_router.route(request)