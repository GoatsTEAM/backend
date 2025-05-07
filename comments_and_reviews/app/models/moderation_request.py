from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class DecisionStatus(str, Enum):
    APPROVED_REVIEW = "approved"
    REJECTED_REVIEW = "rejected"


class Decision(BaseModel):
    moderator_id: str
    status: DecisionStatus
    reason: str
    added_at: datetime = datetime.now()

    @classmethod
    def approve_review(cls, moderator_id: str, reason: str) -> "Decision":
        return cls(
            moderator_id=moderator_id,
            status=DecisionStatus.APPROVED_REVIEW,
            reason=reason,
        )

    @classmethod
    def reject_review(cls, moderator_id: str, reason: str) -> "Decision":
        if not reason:
            raise ValueError("Reason is required")
        return cls(
            moderator_id=moderator_id,
            status=DecisionStatus.REJECTED_REVIEW,
            reason=reason,
        )


class ModerationRequest(BaseModel):
    id: str
    review_id: str
    description: str
    created_at: datetime = datetime.now()
    decision: Decision | None = None

    def close(self, decision: Decision) -> "ModerationRequest":
        if self.decision is not None:
            raise ValueError("Request already closed")
        return self.model_copy(update={"decision": decision})

    def is_opened(self) -> bool:
        return self.decision is None

    def get_decision(self) -> Decision:
        if self.is_opened():
            raise ValueError("Request is not closed")
        return self.decision  # type: ignore
