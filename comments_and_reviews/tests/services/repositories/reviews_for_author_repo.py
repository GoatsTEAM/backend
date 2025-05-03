from bson.objectid import ObjectId

from app.models.review import (
    Review,
    ReviewForAuthor,
    ReviewImpl,
    ReviewStatus,
)
from app.repositories.reviews_repository import (
    ReviewsRepositoryForAuthor,
)


class ReviewsForAuthorRepo(
    ReviewsRepositoryForAuthor,
):
    def __init__(self):
        self.buffer: list[Review] = []

    async def save(self, review):
        self.buffer.append(review)

    async def get_reviews_by_product_id(self, product_id) -> list[Review]:
        return [
            review
            for review in self.buffer
            if review.to_dict()["product_id"] == product_id
        ]

    async def get_review_for_author_by_id(self, id):
        for review in self.buffer:
            if review.to_dict()["id"] == id and isinstance(
                review, ReviewForAuthor
            ):
                return review
        return None

    async def create(self, author, content, metadata) -> Review:
        review = ReviewImpl(
            ObjectId(), author, ReviewStatus.PENDING, content, None, 0, metadata
        )
        self.buffer.append(review)
        return review

    async def delete(self, author_id, review_id):
        self.buffer = [
            review
            for review in self.buffer
            if review.to_dict()["id"] != review_id
            or review.to_dict()["author"]["id"] != author_id
        ]
