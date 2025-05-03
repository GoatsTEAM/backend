from app.models.review import (
    Review,
)

from app.models.review import ReviewForModerator
from app.repositories.reviews_repository import ReviewsRepositoryForModerators


class ReviewsForModeratorsRepo(ReviewsRepositoryForModerators):
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

    async def get_review_for_moderator_by_id(self, id):
        for review in self.buffer:
            if review.to_dict()["id"] == id and isinstance(
                review, ReviewForModerator
            ):
                return review
        return None
