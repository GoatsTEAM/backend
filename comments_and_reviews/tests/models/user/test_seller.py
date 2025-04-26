def test_seller_is_not_moderator(seller):
    assert not seller.is_moderator()


def test_seller_to_dict(seller):
    dict = seller.to_dict()
    assert dict["id"] == seller.id
    assert dict["name"] == seller.name
    assert dict["banned"] == seller.banned


def test_seller_ban(seller):
    assert not seller.is_banned()
    seller.ban()
    assert seller.is_banned()


def test_seller_unban(banned_seller):
    assert banned_seller.is_banned()
    banned_seller.unban()
    assert not banned_seller.is_banned()
