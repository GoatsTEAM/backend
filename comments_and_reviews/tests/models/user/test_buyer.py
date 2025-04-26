def test_buyer_is_not_moderator(buyer):
    assert not buyer.is_moderator()


def test_buyer_to_dict(buyer):
    dict = buyer.to_dict()
    assert dict["id"] == buyer.id
    assert dict["name"] == buyer.name
    assert dict["banned"] == buyer.banned
    assert dict["avatar"] == buyer.avatar


def test_buyer_ban(buyer):
    assert not buyer.is_banned()
    buyer.ban()
    assert buyer.is_banned()


def test_buyer_unban(banned_buyer):
    assert banned_buyer.is_banned()
    banned_buyer.unban()
    assert not banned_buyer.is_banned()
