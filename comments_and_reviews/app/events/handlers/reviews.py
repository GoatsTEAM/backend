from enum import Enum
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
from app.services import ServicesFactory
from app.dependencies.actor import get_actor


class EventType(str, Enum):
    CREATE_REVIEW = "create_review"
    UPDATE_REVIEW = "update_review"
    DELETE_REVIEW = "delete_review"
    GET_REVIEWS_BY_PRODUCT = "get_reviews_by_product"
    GET_REVIEWS_BY_USER = "get_reviews_by_user"
    GET_REVIEW_BY_ID = "get_review_by_id"
    GET_PRODUCT_STATS = "get_product_stats"


async def update_stats(
    services: ServicesFactory,
    new: Review | None = None,
    old: Review | None = None,
):
    if new is not None:
        product_id = new.get_product()
    elif old is not None:
        product_id = old.get_product()
    new_rating = new.get_rating() if new is not None else None
    old_rating = old.get_rating() if old is not None else None
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
