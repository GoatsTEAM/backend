import pytest

from app.repositories.reviews_repository import (
    ReviewsRepositoryForAuthor,
    ReviewsRepositoryForBuyers,
    ReviewsRepositoryForModerators,
    ReviewsRepositoryForSellers,
)
from app.repositories.users_repository import UsersRepository
from app.services.reviews_service import ReviewsService

from tests.services.repositories import (
    ReviewsForAuthorRepo,
    ReviewsForBuyersRepo,
    ReviewsForModeratorsRepo,
    ReviewsForSellersRepo,
    UsersRepo,
)


@pytest.fixture
def reviews_for_author_repo() -> ReviewsRepositoryForAuthor:
    return ReviewsForAuthorRepo()


@pytest.fixture
def reviews_for_buyers_repo() -> ReviewsRepositoryForBuyers:
    return ReviewsForBuyersRepo()


@pytest.fixture
def reviews_for_moderators_repo() -> ReviewsRepositoryForModerators:
    return ReviewsForModeratorsRepo()


@pytest.fixture
def reviews_for_sellers_repo() -> ReviewsRepositoryForSellers:
    return ReviewsForSellersRepo()


@pytest.fixture
def users_repo() -> UsersRepository:
    return UsersRepo()


@pytest.fixture
def review_service(reviews_for_author_repo, users_repo):
    return ReviewsService(reviews_for_author_repo, users_repo)
