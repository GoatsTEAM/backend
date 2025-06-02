from collections import defaultdict
from typing import Callable, Awaitable, Type, Any

from app.events.schemas.event import Event, EventType
from app.services import ServicesFactory
from pydantic import BaseModel


class Router:
    def __init__(self, services: ServicesFactory | None = None):
        self.handlers: dict[EventType, list[tuple[Type[BaseModel], Callable[[Any, ServicesFactory], Awaitable[Any]]]]] = defaultdict(list)
        self.services = services

    def include(self, router: "Router") -> None:
        for event_type, handlers in router.handlers.items():
            self.handlers[event_type].extend(handlers)

    def add(
        self,
        event_type: EventType,
        schema: Type[BaseModel],
    ):
        def decorator(func: Callable[[Any, ServicesFactory], Awaitable[Any]]):
            self.handlers[event_type].append((schema, func))
            return func

        return decorator

    async def route(self, event: Event):
        if event.event_type not in self.handlers:
            return

        for schema, handler in self.handlers[event.event_type]:
            data = schema(**event.body)
            await handler(data, self.services)