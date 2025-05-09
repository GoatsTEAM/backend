from pydantic import BaseModel

from app.events.handlers.base import Handler, ProtectedHandler, EventHandler
from app.events.event_handlers_mapper import EventHandlersMapper
from app.schemas.event import Event
from app.services import ServicesFactory


class Router:
    def __init__(self, services: ServicesFactory):
        self.handlers: dict[str, EventHandler] = {}
        self.services = services

    def add(self, event_type: str, body_model: type[BaseModel]):
        def decorator(func: Handler) -> Handler:
            handler = EventHandlersMapper.wrap_unprotected(func, body_model)
            self.handlers[event_type] = handler
            return func

        return decorator

    def add_protected(self, event_type: str, body_model: type[BaseModel]):
        def decorator(func: ProtectedHandler) -> ProtectedHandler:
            handler = EventHandlersMapper.wrap_protected(func, body_model)
            self.handlers[event_type] = handler
            return func

        return decorator

    async def route(self, event: Event) -> Event:
        handler = self.handlers.get(event.event_type)
        if not handler:
            event.body = {
                "error": f"No handler for event type {event.event_type}"
            }
            return event

        return await handler(event, self.services)
