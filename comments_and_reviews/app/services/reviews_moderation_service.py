from app.models.actor import Actor
from app.models.moderation_request import ModerationRequest, Decision
from app.repositories.moderation_requests_repository import (
    ModerationRequestsRepository,
)
from app.repositories.reviews_repository import ReviewsRepository


class ReviewsModerationService:
    def __init__(
        self,
        moderation_requests_repository: ModerationRequestsRepository,
        reviews_repository: ReviewsRepository,
    ):
        self.requests = moderation_requests_repository
        self.reviews = reviews_repository

    async def create_request(
        self, complainant: Actor, review_id: str, description: str
    ) -> ModerationRequest:
        review = await self.reviews.get_review_by_id(review_id)
        if review is None:
            raise ValueError("Review not found")

        if not (
            review.check_author(complainant.id)
            or complainant.is_seller()
            or complainant.is_moderator()
        ):
            raise ValueError(
                "Only author, seller or moderator can create request"
            )

        request = await self.requests.create_moderation_request(
            review_id, description
        )
        await self.reviews.save(review.to_moderation())
        return request

    async def get_requests(self, moderator: Actor) -> list[ModerationRequest]:
        if not moderator.is_moderator():
            raise ValueError("Only moderator can get requests")
        return await self.requests.get_opened_moderation_requests()

    async def get_request_by_id(
        self, request_id: str
    ) -> ModerationRequest | None:
        return await self.requests.get_moderation_request_by_id(request_id)

    async def approve_review(
        self, moderator: Actor, request_id: str, reason: str
    ):
        if not moderator.is_moderator():
            raise ValueError("Only moderator can approve review")

        request = await self.requests.get_moderation_request_by_id(request_id)
        if request is None:
            raise ValueError("Request not found")

        review = await self.reviews.get_review_by_id(request.review_id)
        if review is None:
            raise ValueError("Review not found")

        decision = Decision.approve_review(moderator.id, reason)
        await self.requests.save(request.close(decision))
        await self.reviews.save(review.publish())

    async def reject_review(
        self, moderator: Actor, request_id: str, reason: str
    ):
        if not moderator.is_moderator():
            raise ValueError("Only moderator can reject review")

        request = await self.requests.get_moderation_request_by_id(request_id)
        if request is None:
            raise ValueError("Request not found")

        review = await self.reviews.get_review_by_id(request.review_id)
        if review is None:
            raise ValueError("Review not found")

        decision = Decision.reject_review(moderator.id, reason)
        await self.requests.save(request.close(decision))
        await self.reviews.save(review.hide())
