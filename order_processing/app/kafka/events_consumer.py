import json
from aiokafka import AIOKafkaConsumer
from app.events.schemas.event import Event


class KafkaConsumer:
    def __init__(self, topic: str, bootstrap_servers: str = "kafka:9092"):
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self._consumer: AIOKafkaConsumer | None = None

    async def start(self):
        if not self._consumer:
            self._consumer = AIOKafkaConsumer(
                self.topic,
                bootstrap_servers=self.bootstrap_servers,
                auto_offset_reset="latest",
                enable_auto_commit=True,
                group_id="cart-service"
            )
            await self._consumer.start()

    async def stop(self):
        if self._consumer:
            await self._consumer.stop()
            self._consumer = None

    async def events(self):
        if not self._consumer:
            await self.start()

        async for msg in self._consumer:
            try:
                event_data = json.loads(msg.value.decode("utf-8"))
                yield Event(**event_data)
            except Exception as e:
                print("Invalid event:", e)