from app.models.ModerationRequest import (
    ModerationRequest,
    ModerationRequestStatus,
)


def test_moderation_request_to_dict(moderation_request):
    assert moderation_request.to_dict() == {
        "id": moderation_request.id,
        "review": moderation_request.review,
        "complainant": moderation_request.complainant,
        "complainee": moderation_request.complainee,
        "description": moderation_request.description,
        "created_at": moderation_request.created_at,
        "closed_at": moderation_request.closed_at,
        "moderator": moderation_request.moderator,
        "status": moderation_request.status,
    }


def test_moderation_request_get_complainee(moderation_request):
    assert moderation_request.get_complainee() == moderation_request.complainee


def test_moderation_request_reject(moderation_request):
    moderation_request.reject()
    assert moderation_request.status == ModerationRequestStatus.REJECTED
    assert not moderation_request.get_complainee().is_banned()


def test_moderation_request_reject_and_ban(moderation_request):
    moderation_request.reject_and_ban()
    assert moderation_request.status == ModerationRequestStatus.REJECTED
    assert moderation_request.get_complainee().is_banned()


def test_moderation_request_approve(moderation_request):
    moderation_request.approve()
    assert moderation_request.status == ModerationRequestStatus.APPROVED
    assert not moderation_request.get_complainee().is_banned()
