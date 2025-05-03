from bson.objectid import ObjectId
from app.repositories.reviews_repository import ReviewsRepositoryForBuyers
from app.repositories.users_repository import UsersRepository


class ReviewInteractionsService:
    def __init__(
        self,
        reviews_repository: ReviewsRepositoryForBuyers,
        users_repository: UsersRepository,
    ):
        self.reviews = reviews_repository
        self.users = users_repository

    async def like_review(self, user_id: int, review_id: ObjectId):
        user = await self.users.get_buyer_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        if user.is_banned():
            raise ValueError("User is banned")

        await self.reviews.like(user_id, review_id)

    async def dislike_review(self, user_id: int, review_id: ObjectId):
        user = await self.users.get_buyer_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        if user.is_banned():
            raise ValueError("User is banned")

        await self.reviews.dislike(user_id, review_id)
