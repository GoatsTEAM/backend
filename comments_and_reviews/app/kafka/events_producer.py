import socket
from confluent_kafka import Producer

from app.events.schemas.event import Event


class EventsProducer:
    def __init__(self, bootstrap_servers: str, topic: str):
        conf = {
            "bootstrap.servers": bootstrap_servers,
            "client.id": socket.gethostname(),
        }
        self.producer = Producer(conf)
        self.topic = topic

    def produce(self, event: Event):
        self.producer.produce(
            self.topic, key=event.token, value=event.model_dump_json()
        )
        self.producer.poll(1)
