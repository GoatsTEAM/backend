from app.events.handlers import BaseEventHandler
from app.schemas.event import Event


class Router:
    def __init__(self):
        self.handlers: dict[str, BaseEventHandler] = {}

    async def route(self, event: Event):
        handler = self.handlers.get(event.event_type)
        if handler is None:
            raise ValueError(f"Handler for event {event.event_type} not found")

        return await handler.handle(event)
