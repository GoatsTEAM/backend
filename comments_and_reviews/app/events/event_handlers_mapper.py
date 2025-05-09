from functools import wraps
from pydantic import BaseModel

from app.events.handlers.base import Handler, ProtectedHandler, EventHandler
from app.services import ServicesFactory
from app.schemas.event import Event


class EventHandlersMapper:
    @staticmethod
    def wrap_unprotected(
        func: Handler, body_model: type[BaseModel]
    ) -> EventHandler:
        @EventHandlersMapper._handle_errors
        async def wrapper(event: Event, services: ServicesFactory) -> Event:
            body_obj = body_model.model_validate(event.body)
            result = await func(body_obj, services)
            event.body = result.model_dump()
            return event

        return wrapper

    @staticmethod
    def wrap_protected(
        func: ProtectedHandler, body_model: type[BaseModel]
    ) -> EventHandler:
        @EventHandlersMapper._handle_errors
        async def wrapper(event: Event, services: ServicesFactory) -> Event:
            if event.access_token is None:
                raise ValueError("Access token is required")
            body_obj = body_model.model_validate(event.body)
            result = await func(event.access_token, body_obj, services)
            event.body = result.model_dump()
            return event

        return wrapper

    @staticmethod
    def _handle_errors(func: EventHandler) -> EventHandler:
        @wraps(func)
        async def wrapper(event: Event, services: ServicesFactory) -> Event:
            try:
                return await func(event, services)
            except Exception as e:
                event.body = {"error": str(e)}
                return event

        return wrapper
