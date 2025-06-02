from pydantic import BaseModel
from app.models.review import ReviewContent, Review


class CreateReview(BaseModel):
    product_id: str
    content: ReviewContent


class UpdateReview(BaseModel):
    review_id: str
    content: ReviewContent


class Id(BaseModel):
    value: str


class ReadReviews(BaseModel):
    reviews: list[Review]
