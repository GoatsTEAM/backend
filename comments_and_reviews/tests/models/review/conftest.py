import pytest

from faker import Faker

from app.models.review import (
    ReviewContent,
    ReviewMetadata,
    ReviewImpl,
    ReviewStatus,
    ReviewForAuthor,
    ReviewForModerator,
    ReviewForSeller,
)
from app.models.user import Buyer
from tests.models.user.conftest import buyer


fake = Faker()


@pytest.fixture
def content():
    n_media = fake.random_int(min=0, max=5)
    return ReviewContent(
        rating=fake.random_int(min=1, max=5),
        text=fake.text(),
        media=[fake.image_url() for _ in range(n_media)],
    )


@pytest.fixture
def answer():
    return fake.text()


@pytest.fixture
def metadata(id):
    edited_at = fake.date_time()
    created_at = fake.date_time(end_datetime=edited_at)
    return ReviewMetadata(
        product_id=id,
        returned_order=False,
        edited_at=edited_at,
        created_at=created_at,
    )


@pytest.fixture
def review(id, buyer, content, answer, metadata):
    return ReviewImpl(
        id=id,
        author=buyer,
        status=ReviewStatus.PUBLISHED,
        content=content,
        answer=answer,
        likes=0,
        metadata=metadata,
    )


@pytest.fixture
def review_with_author(
    id, buyer, content, answer, metadata
) -> tuple[ReviewImpl, Buyer]:
    review = ReviewImpl(
        id=id,
        author=buyer,
        status=ReviewStatus.PUBLISHED,
        content=content,
        answer=answer,
        likes=0,
        metadata=metadata,
    )
    return review, buyer


@pytest.fixture
def review_for_author(review) -> ReviewForAuthor:
    return review


@pytest.fixture
def review_for_seller(review) -> ReviewForSeller:
    return review


@pytest.fixture
def review_for_moderator(review) -> ReviewForModerator:
    return review
