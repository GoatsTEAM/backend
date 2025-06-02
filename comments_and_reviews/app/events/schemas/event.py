from enum import Enum
from pydantic import BaseModel


class EventType(str, Enum):
    CREATE_REVIEW = "create_review"
    UPDATE_REVIEW = "update_review"
    DELETE_REVIEW = "delete_review"
    GET_REVIEWS_BY_PRODUCT = "get_reviews_by_product"
    GET_REVIEWS_BY_USER = "get_reviews_by_user"
    GET_REVIEW_BY_ID = "get_review_by_id"
    GET_PRODUCT_STATS = "get_product_stats"


class Event(BaseModel):
    token: str
    event_type: EventType
    access_token: str | None
    body: dict
