from aiokafka import AIOKafkaProducer
from app.core.config import settings

_kafka_producer: AIOKafkaProducer | None = None

def get_kafka_producer() -> AIOKafkaProducer:
    return _kafka_producer

async def init_kafka_producer():
    global _kafka_producer
    _kafka_producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_bootstrap_servers)
    await _kafka_producer.start()

async def close_kafka_producer():
    global _kafka_producer
    if _kafka_producer:
        await _kafka_producer.stop()
        _kafka_producer = None