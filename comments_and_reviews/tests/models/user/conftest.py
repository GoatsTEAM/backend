import pytest
from faker import Faker
from app.models.User import User, Moderator, Admin, Operator, Seller, Buyer

fake = Faker()


def make(user_cls: type[User], *, banned: bool = False) -> User:
    return user_cls(
        fake.random_int(min=1, max=10000),
        fake.name(),
        banned,
        avatar=fake.image_url(),
    )


@pytest.fixture
def user() -> User:
    return make(User)


@pytest.fixture
def banned_user() -> User:
    return make(User, banned=True)


@pytest.fixture
def admin() -> Admin:
    admin = make(Admin)
    assert isinstance(admin, Admin)
    return admin


@pytest.fixture
def operator() -> Operator:
    op = make(Operator)
    assert isinstance(op, Operator)
    return op


@pytest.fixture
def moderator() -> Moderator:
    moderator = make(Moderator)
    assert isinstance(moderator, Moderator)
    return moderator


@pytest.fixture
def buyer() -> Buyer:
    buyer = make(Buyer)
    assert isinstance(buyer, Buyer)
    return buyer


@pytest.fixture
def seller() -> Seller:
    seller = make(Seller)
    assert isinstance(seller, Seller)
    return seller
