from abc import ABC, abstractmethod

from bson.objectid import ObjectId

from app.models.reviews_statistics import ProductStatistics


class ProductsRepository(ABC):
    @abstractmethod
    async def get_stats(self, product_id: ObjectId) -> ProductStatistics: ...

    @abstractmethod
    async def save(self, stats: ProductStatistics): ...
