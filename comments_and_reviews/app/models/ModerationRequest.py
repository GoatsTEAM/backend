from datetime import datetime
from enum import Enum
from bson.objectid import ObjectId

from app.models.Base import BaseModel
from app.models.Review import ReviewForModerator
from app.models.User import User, Moderator


class ModerationRequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ModerationRequest(BaseModel):
    def __init__(
        self,
        id: ObjectId,
        review: ReviewForModerator,
        created_by: User,
        description: str,
        created_at: datetime,
        closed_at: datetime | None,
        moderator: Moderator,
        status: ModerationRequestStatus,
    ):
        self.id = id
        self.review = review
        self.complainant = created_by
        self.complainee = review.get_author()
        self.description = description
        self.created_at = created_at
        self.closed_at = closed_at
        self.moderator = moderator
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "review": self.review,
            "complainant": self.complainant.to_dict(),
            "complainee": self.complainee.to_dict(),
            "description": self.description,
            "created_at": self.created_at,
            "closed_at": self.closed_at,
            "moderator": self.moderator.to_dict(),
            "status": self.status,
        }

    def reject(self):
        self.status = ModerationRequestStatus.REJECTED
        self.closed_at = datetime.now()
        self.review.hide()

    def reject_and_ban(self):
        self.reject()
        self.moderator.ban_user(self.complainee)

    def approve(self):
        self.status = ModerationRequestStatus.APPROVED
        self.closed_at = datetime.now()
        self.review.publish()

    def get_complainee(self):
        return self.complainee
