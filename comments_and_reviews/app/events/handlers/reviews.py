from app.main import event_router
from app.models.actor import Actor
from app.models.review import Review
from app.models.reviews_statistics import ReviewsStatistics
from app.events.schemas.review import (
    CreateReview,
    UpdateReview,
    ReadReviews,
    Id,
)
from app.events.schemas.event import EventType
from app.services import ServicesFactory
from app.dependencies.actor import get_actor


def get_product_id(new: Review | None, old: Review | None) -> str:
    if new is not None:
        return new.get_product()
    elif old is not None:
        return old.get_product()
    else:
        raise ValueError("New or old review must be provided")


def get_rating(review: Review | None) -> int | None:
    if review is not None:
        return review.get_rating()
    else:
        return None


async def update_stats(
    services: ServicesFactory,
    new: Review | None = None,
    old: Review | None = None,
):
    product_id = get_product_id(new, old)
    new_rating = get_rating(new)
    old_rating = get_rating(old)
    stats = services.get_reviews_statistics_service()
    await stats.update_stats_if_exists(product_id, new_rating, old_rating)


async def add_automoderation_request(
    services: ServicesFactory, complainant: Actor, review_id: str
):
    moderation = services.get_reviews_moderation_service()
    await moderation.create_request(complainant, review_id, "Automoderation")


@event_router.add_protected(EventType.CREATE_REVIEW, CreateReview)
async def handle_create_review(
    token: str, body: CreateReview, services: ServicesFactory
) -> Review:
    actor = get_actor(token)
    reviews = services.get_reviews_service()
    res = await reviews.create_review(actor, **body.model_dump())
    await update_stats(services, new=res)
    await add_automoderation_request(services, actor, res.id)
    return res


@event_router.add_protected(EventType.UPDATE_REVIEW, UpdateReview)
async def handle_update_review(
    token: str, body: UpdateReview, services: ServicesFactory
) -> Review:
    actor = get_actor(token)
    reviews = services.get_reviews_service()
    new, old = await reviews.update_review(actor, **body.model_dump())
    await update_stats(services, new=new, old=old)
    await add_automoderation_request(services, actor, new.id)
    return new


@event_router.add_protected(EventType.DELETE_REVIEW, Id)
async def handle_delete_review(
    token: str, body: Id, services: ServicesFactory
) -> Review:
    actor = get_actor(token)
    reviews = services.get_reviews_service()
    res = await reviews.delete_review(actor, **body.model_dump())
    await update_stats(services, old=res)
    return res


@event_router.add(EventType.GET_REVIEWS_BY_PRODUCT, Id)
async def handle_get_reviews_by_product_id(
    body: Id, services: ServicesFactory
) -> ReadReviews:
    reviews = services.get_reviews_service()
    res = await reviews.get_reviews_by_product(body.value)
    return ReadReviews(reviews=res)


@event_router.add(EventType.GET_REVIEWS_BY_USER, Id)
async def handle_get_reviews_by_user(
    body: Id, services: ServicesFactory
) -> ReadReviews:
    reviews = services.get_reviews_service()
    res = await reviews.get_reviews_by_user(body.value)
    return ReadReviews(reviews=res)


@event_router.add(EventType.GET_REVIEW_BY_ID, Id)
async def handle_get_review_by_id(
    body: Id, services: ServicesFactory
) -> ReadReviews:
    reviews = services.get_reviews_service()
    res = await reviews.get_review_by_id(body.value)
    if res is None:
        return ReadReviews(reviews=[])
    else:
        return ReadReviews(reviews=[res])


@event_router.add(EventType.GET_PRODUCT_STATS, Id)
async def handle_get_product_stats(
    body: Id, services: ServicesFactory
) -> ReviewsStatistics:
    stats = services.get_reviews_statistics_service()
    return await stats.get_stats(body.value)
