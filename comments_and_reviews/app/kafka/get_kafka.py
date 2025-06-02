from app.kafka.events_consumer import EventsConsumer
from app.kafka.events_producer import EventsProducer
from app.core.config import settings


def get_kafka() -> tuple[EventsConsumer, EventsProducer]:
    consumer = EventsConsumer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        topic=settings.KAFKA_REQUEST_TOPIC,
        group_id=settings.KAFKA_GROUP_ID,
    )
    producer = EventsProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        topic=settings.KAFKA_RESPONSE_TOPIC,
    )
    return consumer, producer
