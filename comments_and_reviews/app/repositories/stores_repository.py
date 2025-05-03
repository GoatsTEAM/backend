from abc import ABC, abstractmethod
from bson.objectid import ObjectId

from app.models.reviews_statistics import StoreStatistics


class StoresRepository(ABC):
    @abstractmethod
    async def get_stats(self, store_id: ObjectId) -> StoreStatistics: ...

    @abstractmethod
    async def save(self, stats: StoreStatistics): ...
