from abc import ABC, abstractmethod

from app.models.reviews_statistics import StoreStatistics


class StoresRepository(ABC):
    @abstractmethod
    async def get_stats(self, store_id: int) -> StoreStatistics: ...

    @abstractmethod
    async def save(self, stats: StoreStatistics): ...
