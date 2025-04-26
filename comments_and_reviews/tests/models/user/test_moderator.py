def test_moderator_role(moderator):
    assert moderator.is_moderator()


def test_moderator_to_dict(moderator):
    dict = moderator.to_dict()
    assert dict["id"] == moderator.id
    assert dict["name"] == moderator.name


def test_moderator_bans_bannable(moderator, buyer, seller):
    assert not buyer.is_banned()
    assert not seller.is_banned()

    moderator.ban_user(buyer)
    moderator.ban_user(seller)

    assert buyer.is_banned()
    assert seller.is_banned()


def test_moderator_unbans_bannable(moderator, banned_buyer, banned_seller):
    assert banned_buyer.is_banned()
    assert banned_seller.is_banned()

    moderator.unban_user(banned_buyer)
    moderator.unban_user(banned_seller)

    assert not banned_buyer.is_banned()
    assert not banned_seller.is_banned()
