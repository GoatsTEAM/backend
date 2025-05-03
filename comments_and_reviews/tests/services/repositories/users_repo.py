from bson.objectid import ObjectId
from app.repositories.users_repository import UsersRepository
from app.models.user import User, Buyer, Seller, Moderator


class UsersRepo(UsersRepository):
    def __init__(self):
        self.buyers: list[Buyer] = []
        self.sellers: list[Seller] = []
        self.moderators: list[Moderator] = []

    async def create(self, user: User) -> User:
        if isinstance(user, Buyer):
            self.buyers.append(user)
        elif isinstance(user, Seller):
            self.sellers.append(user)
        elif isinstance(user, Moderator):
            self.moderators.append(user)
        return user

    async def get_buyer_by_id(self, id: ObjectId) -> Buyer | None:
        for buyer in self.buyers:
            if buyer.id == id:
                return buyer
        return None
