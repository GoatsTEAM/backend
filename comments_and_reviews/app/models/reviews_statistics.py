from pydantic import BaseModel, Field


class ReviewsStatistics(BaseModel):
    id: str
    average_rating: float = Field(default=0, ge=0, le=5)
    reviews_count: int = Field(default=0, ge=0)

    def add_review(self, rating: float) -> "ReviewsStatistics":
        new_count = self.reviews_count + 1
        new_rating = (
            self.average_rating * self.reviews_count + rating
        ) / new_count
        return self.model_copy(
            update={
                "average_rating": new_rating,
                "reviews_count": new_count,
            }
        )

    def remove_review(self, rating: float) -> "ReviewsStatistics":
        new_count = self.reviews_count - 1
        new_rating = (
            self.average_rating * self.reviews_count - rating
        ) / new_count
        return self.model_copy(
            update={
                "average_rating": new_rating,
                "reviews_count": new_count,
            }
        )
