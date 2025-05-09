from collections.abc import Awaitable, Callable
from pydantic import BaseModel

from app.services import ServicesFactory
from app.schemas.event import Event


Handler = Callable[[BaseModel, ServicesFactory], Awaitable[BaseModel]]

ProtectedHandler = Callable[
    [str, BaseModel, ServicesFactory], Awaitable[BaseModel]
]

EventHandler = Callable[[Event, ServicesFactory], Awaitable[Event]]
