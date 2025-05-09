from abc import ABC, abstractmethod

from app.schemas.event import Event


class BaseEventHandler(ABC):
    @abstractmethod
    async def handle(self, event: Event) -> Event: ...
