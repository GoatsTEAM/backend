from abc import ABC, abstractmethod

from app.models.reviews_statistics import ProductStatistics


class ProductsRepository(ABC):
    @abstractmethod
    async def get_stats(self, product_id: int) -> ProductStatistics: ...

    @abstractmethod
    async def save(self, stats: ProductStatistics): ...
