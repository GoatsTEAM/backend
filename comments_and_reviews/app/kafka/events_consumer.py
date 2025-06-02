import asyncio
from confluent_kafka import Consumer
from collections.abc import AsyncGenerator

from app.events.schemas.event import Event


class EventsConsumer:
    def __init__(self, topic: str, group_id: str, bootstrap_servers: str):
        conf = {
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest",
        }
        self.consumer = Consumer(conf)
        self.consumer.subscribe([topic])

    async def events(self) -> AsyncGenerator[Event, None]:
        loop = asyncio.get_running_loop()
        try:
            while True:
                event = await loop.run_in_executor(None, self._poll_event)
                if event is None:
                    continue
                yield event
        finally:
            self.consumer.close()

    def _poll_event(self) -> Event | None:
        message = self.consumer.poll(1.0)
        if message is None:
            return None
        if message.error():
            raise RuntimeError(f"Kafka error: {message.error()}")
        else:
            return self._deserialize(message)

    def _deserialize(self, message) -> Event:
        content = message.value().decode("utf-8")
        return Event.model_validate_json(content)
