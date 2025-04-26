from bson.objectid import ObjectId

from app.models.Base import BaseModel


class Reviewable(BaseModel):
    def __init__(self, id: ObjectId, average_rating: int, reviews_count: int):
        self.id = id
        self.average_rating = average_rating
        self.reviews_count = reviews_count

    def to_dict(self):
        return {
            "id": self.id,
            "average_rating": self.average_rating,
            "reviews_count": self.reviews_count,
        }

    def add_review(self, rating: int):
        self.average_rating = (
            self.average_rating * self.reviews_count + rating
        ) / (self.reviews_count + 1)
        self.reviews_count += 1

    def update_review(self, old_rating: int, new_rating: int):
        if self.reviews_count == 0:
            return

        self.average_rating = (
            self.average_rating * self.reviews_count - old_rating + new_rating
        ) / self.reviews_count

    def delete_review(self, rating: int):
        if self.reviews_count <= 1:
            self.average_rating = 0
            self.reviews_count = 0
        else:
            self.average_rating = (
                self.average_rating * self.reviews_count - rating
            ) / (self.reviews_count - 1)
            self.reviews_count -= 1


class Product(Reviewable):
    pass


class Store(Reviewable):
    pass
