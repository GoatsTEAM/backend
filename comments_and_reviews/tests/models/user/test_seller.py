def test_seller_is_not_moderator(seller):
    assert not seller.is_moderator()


def test_seller_to_dict(seller):
    dict = seller.to_dict()
    assert dict["id"] == seller.id
    assert dict["name"] == seller.name
    assert dict["banned"] == seller.banned
