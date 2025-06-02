from collections.abc import Awaitable, Callable
from typing import TypeVar
from pydantic import BaseModel

from app.services import ServicesFactory
from app.events.schemas.event import Event

T = TypeVar("T", bound=BaseModel)

Handler = Callable[[T, ServicesFactory], Awaitable[BaseModel]]

ProtectedHandler = Callable[[str, T, ServicesFactory], Awaitable[BaseModel]]

EventHandler = Callable[[Event, ServicesFactory], Awaitable[Event]]
