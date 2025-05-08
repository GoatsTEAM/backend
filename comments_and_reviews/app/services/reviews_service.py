from app.models.review import ReviewContent, ReviewMetadata, Review
from app.models.actor import Actor
from app.repositories.reviews_repository import ReviewsRepository
from app.repositories.reviews_statistics_repository import (
    ReviewsStatisticsRepository,
)


async def get_metadata(product_id: str) -> ReviewMetadata:
    # TODO:
    # check if product exists
    # get order status
    return ReviewMetadata(product_id=product_id)


class ReviewsService:
    def __init__(
        self,
        reviews_repository: ReviewsRepository,
        reviews_statistics_repository: ReviewsStatisticsRepository,
    ):
        self.reviews = reviews_repository
        self.stats = reviews_statistics_repository

    async def create_review(
        self, product_id: str, author: Actor, content: ReviewContent
    ) -> Review:
        if not author.is_buyer():
            raise ValueError("Only buyer can create review")

        metadata = await get_metadata(product_id)
        return await self.reviews.create_review(
            author_id=author.id,
            content=content,
            metadata=metadata,
        )

    async def update_review(
        self, author: Actor, review_id: str, content: ReviewContent
    ) -> tuple[Review, Review]:
        if not author.is_buyer():
            raise ValueError("Only buyer can update review")

        old_review = await self.reviews.get_review_by_id(review_id)
        if old_review is None:
            raise ValueError("Review not found")

        if not old_review.check_author(author.id):
            raise ValueError("Only author can update review")

        new_review = old_review.update_content(content)
        await self.reviews.save(new_review)
        return new_review, old_review

    async def delete_review(self, author: Actor, review_id: str) -> Review:
        if not author.is_buyer():
            raise ValueError("Only buyer can delete review")

        review = await self.reviews.get_review_by_id(review_id)
        if review is None:
            raise ValueError("Review not found")

        if not review.check_author(author.id):
            raise ValueError("Only author can delete review")

        await self.reviews.save(review.hide())
        return review

    async def get_reviews_by_product(self, product_id: str) -> list[Review]:
        return await self.reviews.get_reviews_by_product_id(product_id)

    async def get_reviews_by_author(self, author: Actor) -> list[Review]:
        if not author.is_buyer():
            raise ValueError("Only buyer can get reviews by author")
        return await self.reviews.get_reviews_by_author_id(author.id)

    async def get_review_by_id(self, review_id: str) -> Review | None:
        return await self.reviews.get_review_by_id(review_id)
