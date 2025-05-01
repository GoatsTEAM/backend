def test_moderator_role(moderator):
    assert moderator.is_moderator()


def test_moderator_to_dict(moderator):
    dict = moderator.to_dict()
    assert dict["id"] == moderator.id
    assert dict["name"] == moderator.name


def test_moderator_bans_buyer(moderator, buyer):
    assert not buyer.is_banned()
    moderator.ban_user(buyer)
    assert buyer.is_banned()


def test_moderator_unbans_buyer(moderator, banned_buyer):
    assert banned_buyer.is_banned()
    moderator.unban_user(banned_buyer)
    assert not banned_buyer.is_banned()
