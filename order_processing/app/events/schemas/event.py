from pydantic import BaseModel
from enum import Enum


class EventType(str, Enum):
    ADD_TO_CART = "add_to_cart"

class Event(BaseModel):
    event_type: EventType
    token: str | None = None
    body: dict