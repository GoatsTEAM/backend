import pytest

from faker import Faker

from app.models.Reviewable import Reviewable

fake = Faker()


@pytest.fixture
def empty_reviewable(id) -> Reviewable:
    return Reviewable(id, 0, 0)


@pytest.fixture
def rating() -> int:
    return fake.random_int(min=1, max=5)


@pytest.fixture
def ratings() -> list[int]:
    return [fake.random_int(min=1, max=5) for _ in range(100)]
