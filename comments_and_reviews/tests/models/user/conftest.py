import pytest
from faker import Faker
from app.models.User import Moderator, Seller, Buyer

fake = Faker()


@pytest.fixture
def moderator(id) -> Moderator:
    return Moderator(id=id, name=fake.name())


@pytest.fixture
def buyer(id) -> Buyer:
    return Buyer(
        id=id,
        name=fake.name(),
        banned=False,
        avatar=fake.image_url(),
    )


@pytest.fixture
def banned_buyer(buyer) -> Buyer:
    buyer.ban()
    return buyer


@pytest.fixture
def seller(id) -> Seller:
    return Seller(id=id, name=fake.name(), banned=False)


@pytest.fixture
def banned_seller(seller) -> Seller:
    seller.ban()
    return seller
