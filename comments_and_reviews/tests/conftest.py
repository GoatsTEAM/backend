import pytest
from bson.objectid import ObjectId


@pytest.fixture
def id() -> ObjectId:
    return ObjectId()
