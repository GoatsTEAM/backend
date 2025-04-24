class Reviewable:
    id: int
    average_rating: float
    reviews_count: int

    def __init__(self, id: int, average_rating: int, reviews_count: int):
        self.id = id
        self.average_rating = average_rating
        self.reviews_count = reviews_count

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

    def get_rating_info(self) -> tuple[int, float]:
        return self.reviews_count, self.average_rating


class Product(Reviewable):
    pass


class Store(Reviewable):
    pass
