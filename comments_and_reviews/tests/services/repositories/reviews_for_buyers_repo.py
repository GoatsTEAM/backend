from bson.objectid import ObjectId

from app.models.review import (
    Review,
    ReviewImpl,
)
from app.repositories.reviews_repository import (
    ReviewsRepositoryForBuyers,
)


class ReviewsForBuyersRepo(
    ReviewsRepositoryForBuyers,
):
    def __init__(self):
        self.likes: dict[ObjectId, list[ObjectId]] = {}
        self.buffer: list[Review] = []

    async def save(self, review):
        self.buffer.append(review)

    async def get_reviews_by_product_id(self, product_id) -> list[Review]:
        return [
            review
            for review in self.buffer
            if review.to_dict()["product_id"] == product_id
        ]

    async def like(self, user_id: ObjectId, review_id: ObjectId):
        if user_id in self.likes[review_id]:
            return

        for i, review in enumerate(self.buffer):
            if review.to_dict()["id"] == review_id:
                self.buffer[i] = ReviewImpl(
                    review.to_dict()["id"],
                    review.to_dict()["author"],
                    review.to_dict()["status"],
                    review.to_dict()["content"],
                    review.to_dict()["answer"],
                    review.to_dict()["likes"] + 1,
                    review.to_dict()["metadata"],
                )
        self.likes[review_id].append(user_id)

    async def dislike(self, user_id, review_id):
        if user_id not in self.likes[review_id]:
            return

        for i, review in enumerate(self.buffer):
            if review.to_dict()["id"] == review_id:
                self.buffer[i] = ReviewImpl(
                    review.to_dict()["id"],
                    review.to_dict()["author"],
                    review.to_dict()["status"],
                    review.to_dict()["content"],
                    review.to_dict()["answer"],
                    review.to_dict()["likes"] - 1,
                    review.to_dict()["metadata"],
                )
        self.likes[review_id].remove(user_id)
