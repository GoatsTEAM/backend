from app.repositories.reviews_repository import ReviewsRepository
from app.models.review import (
    ReviewContent,
    ReviewMetadata,
    Review,
    ReviewStatus,
)
from app.models.reviews_statistics import ReviewsStatistics
from app.db.mongo.models.review_document import ReviewDocument


class ReviewsRepositoryBeanie(ReviewsRepository):
    async def create_review(
        self, author_id: str, content: ReviewContent, metadata: ReviewMetadata
    ) -> Review:
        new_review = ReviewDocument(
            author_id=author_id, content=content, metadata=metadata
        )
        new_review = await new_review.insert()
        return new_review.to_review()

    async def get_review_by_id(self, review_id: str) -> Review | None:
        result = await ReviewDocument.get(review_id)
        if result is None:
            return None
        else:
            return result.to_review()

    async def save(self, review: Review):
        document = ReviewDocument.from_review(review)
        await document.save()

    async def get_published_reviews_by_product_id(
        self, product_id: str
    ) -> list[Review]:
        result = await ReviewDocument.find(
            ReviewDocument.metadata.product_id == product_id,
            ReviewDocument.status == ReviewStatus.PUBLISHED,
        ).to_list()
        return [review.to_review() for review in result]

    async def get_reviews_by_author_id(self, author_id: str) -> list[Review]:
        result = await ReviewDocument.find(
            ReviewDocument.author_id == author_id
        ).to_list()
        return [review.to_review() for review in result]

    async def calculate_stats(self, product_id: str) -> ReviewsStatistics:
        filter_query = ReviewDocument.find(
            ReviewDocument.metadata.product_id == product_id,
            ReviewDocument.status == ReviewStatus.PUBLISHED,
        )
        stats = await filter_query.aggregate(
            [
                {
                    "$group": {
                        "_id": "$metadata.product_id",
                        "avg_rating": {"$avg": "$metadata.rating"},
                        "count": {"$sum": 1},
                    }
                }
            ]
        ).to_list()

        if not stats:
            return ReviewsStatistics(id=product_id)

        return ReviewsStatistics(
            id=product_id,
            average_rating=stats[0].get("avg_rating", 0),
            reviews_count=stats[0].get("count", 0),
        )
