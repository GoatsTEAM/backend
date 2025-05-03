from datetime import datetime
from bson.objectid import ObjectId
from app.repositories.reviews_repository import ReviewsRepositoryForAuthor
from app.repositories.users_repository import UsersRepository
from app.models.review import (
    Review,
    ReviewContent,
    ReviewMetadata,
)
from app.models.user import Buyer


async def get_metadata(product_id: ObjectId) -> ReviewMetadata:
    # TODO: check if product exists
    # TODO: get order status
    return ReviewMetadata(product_id, False, datetime.now(), datetime.now())


async def get_user_info(user_id: ObjectId) -> Buyer:
    # TODO: check if user exists and not banned
    # TODO: get user data
    return Buyer(user_id, "John Doe", False, "")


class ReviewsService:
    def __init__(
        self,
        reviews_repository: ReviewsRepositoryForAuthor,
        users_repository: UsersRepository,
    ):
        self.reviews = reviews_repository
        self.users = users_repository

    async def create_review(
        self, author_id: ObjectId, product_id: ObjectId, content: ReviewContent
    ) -> Review:
        user = await self.users.get_buyer_by_id(author_id)
        if user is None:
            user = await get_user_info(author_id)
            user = self.users.create(user)
            assert isinstance(user, Buyer)

        if user.is_banned():
            raise ValueError("User is banned")

        metadata = await get_metadata(product_id)
        return await self.reviews.create(user, content, metadata)

    async def update_review(
        self, author_id: ObjectId, review_id: ObjectId, content: ReviewContent
    ) -> Review:
        user = await self.users.get_buyer_by_id(author_id)
        if user is None:
            raise ValueError("User not found")
        if user.is_banned():
            raise ValueError("User is banned")

        review = await self.reviews.get_review_for_author_by_id(review_id)
        if review is None:
            raise ValueError("Review not found")

        review.update(content)
        await self.reviews.save(review)
        return review

    async def delete_review(self, author_id: ObjectId, review_id: ObjectId):
        await self.reviews.delete(author_id, review_id)
