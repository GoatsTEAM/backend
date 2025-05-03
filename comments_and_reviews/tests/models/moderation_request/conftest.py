import pytest
from faker import Faker

from app.models.moderation_request import (
    ModerationRequest,
    ModerationRequestStatus,
)

from tests.models.user.conftest import *
from tests.models.review.conftest import *

fake = Faker()


@pytest.fixture
def moderation_request(
    id, review_for_moderator, seller, moderator
) -> ModerationRequest:
    return ModerationRequest(
        id=id,
        review=review_for_moderator,
        created_by=seller,
        description=fake.text(),
        created_at=fake.date_time(),
        closed_at=None,
        moderator=moderator,
        status=ModerationRequestStatus.PENDING,
    )
