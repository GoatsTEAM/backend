from bson.objectid import ObjectId
from app.repositories.reviews_repository import ReviewsRepository
from app.repositories.products_repository import ProductsRepository
from app.repositories.stores_repository import StoresRepository
from app.models.review import Review
from app.models.reviews_statistics import ProductStatistics, StoreStatistics


class ProductReviewsService:
    def __init__(
        self,
        reviews_repository: ReviewsRepository,
        products_repository: ProductsRepository,
        stores_repository: StoresRepository,
    ):
        self.reviews = reviews_repository
        self.products = products_repository
        self.stores = stores_repository

    async def get_reviews(self, product_id: ObjectId) -> list[Review]:
        return await self.reviews.get_reviews_by_product_id(product_id)

    async def get_product_stats(
        self, product_id: ObjectId
    ) -> ProductStatistics:
        return await self.products.get_stats(product_id)

    async def get_store_stats(self, store_id: ObjectId) -> StoreStatistics:
        return await self.stores.get_stats(store_id)
