import pytest


def test_reviewable_to_dict(empty_reviewable):
    empty_reviewable.add_review(5)
    dict = empty_reviewable.to_dict()
    assert dict["id"] == empty_reviewable.id
    assert dict["average_rating"] == empty_reviewable.average_rating
    assert dict["reviews_count"] == empty_reviewable.reviews_count


def test_add_first_review(empty_reviewable, rating):
    empty_reviewable.add_review(rating)
    dict = empty_reviewable.to_dict()
    count, avg = dict["reviews_count"], dict["average_rating"]
    assert count == 1
    assert pytest.approx(avg, rel=1e-9) == rating


def test_delete_review_from_empty_reviewable(empty_reviewable, rating):
    empty_reviewable.delete_review(rating)
    dict = empty_reviewable.to_dict()
    count, avg = dict["reviews_count"], dict["average_rating"]
    assert count == 0
    assert pytest.approx(avg, rel=1e-9) == 0


def test_update_empty_reviewable(empty_reviewable, rating):
    empty_reviewable.update_review(rating, rating)
    dict = empty_reviewable.to_dict()
    count, avg = dict["reviews_count"], dict["average_rating"]
    assert count == 0
    assert pytest.approx(avg, rel=1e-9) == 0


def test_add_many_reviews(empty_reviewable, ratings):
    for rating in ratings:
        empty_reviewable.add_review(rating)
    dict = empty_reviewable.to_dict()
    count, avg = dict["reviews_count"], dict["average_rating"]
    assert count == len(ratings)
    assert pytest.approx(avg, rel=1e-9) == sum(ratings) / len(ratings)


def test_delete_from_many_reviews(empty_reviewable, ratings):
    for rating in ratings:
        empty_reviewable.add_review(rating)
    empty_reviewable.delete_review(ratings[0])

    dict = empty_reviewable.to_dict()
    count, avg = dict["reviews_count"], dict["average_rating"]
    assert count == len(ratings[1:])
    assert pytest.approx(avg, rel=1e-9) == sum(ratings[1:]) / len(ratings[1:])


def test_delete_many_reviews(empty_reviewable, ratings):
    for rating in ratings:
        empty_reviewable.add_review(rating)
    for rating in ratings:
        empty_reviewable.delete_review(rating)
    dict = empty_reviewable.to_dict()
    count, avg = dict["reviews_count"], dict["average_rating"]
    assert count == 0
    assert pytest.approx(avg, rel=1e-9) == 0


def test_update_review(empty_reviewable, ratings, rating):
    for r in ratings:
        empty_reviewable.add_review(r)
    empty_reviewable.update_review(ratings[0], rating)

    dict = empty_reviewable.to_dict()
    count, avg = dict["reviews_count"], dict["average_rating"]
    assert count == len(ratings)
    assert pytest.approx(avg, rel=1e-9) == (rating + sum(ratings[1:])) / len(
        ratings
    )


def test_update_many_reviews(empty_reviewable, ratings):
    for rating in ratings[1:]:
        empty_reviewable.add_review(rating)
    for rating in ratings[1:]:
        empty_reviewable.update_review(rating, ratings[0])
    dict = empty_reviewable.to_dict()
    count, avg = dict["reviews_count"], dict["average_rating"]
    assert count == len(ratings[1:])
    assert pytest.approx(avg, rel=1e-9) == ratings[0]
