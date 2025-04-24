from app.models.User import User, Buyer, Moderator


def test_user_demote_to_buyer(user):
    assert isinstance(user.demote_to_buyer(), Buyer)


def test_moderator_unban(moderator, banned_user):
    assert banned_user.isBanned()
    unbanned = moderator.unban(banned_user)
    assert not unbanned.isBanned()


def test_admin_bans_moderator_and_downgrade(admin, moderator):
    banned = admin.ban(moderator)
    assert isinstance(banned, Buyer)
    assert banned.isBanned()


def test_operator_cant_ban_moderator(operator, moderator):
    banned = operator.ban(moderator)
    assert isinstance(banned, Moderator)
    assert not banned.isBanned()


def test_admin_bans_not_moderator(admin, buyer, seller):
    assert_not_moderator_banned(admin, buyer)
    assert_not_moderator_banned(admin, seller)


def test_operator_bans_not_moderators(operator, buyer, seller):
    assert_not_moderator_banned(operator, buyer)
    assert_not_moderator_banned(operator, seller)


def assert_not_moderator_banned(moderator: Moderator, target_user: User):
    assert not isinstance(target_user, Moderator)
    banned = moderator.ban(target_user)
    assert isinstance(banned, type(target_user))
    assert banned.isBanned()
