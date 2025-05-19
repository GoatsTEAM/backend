from pydantic import BaseModel


class Event(BaseModel):
    token: str
    event_type: str
    access_token: str | None
    body: dict
