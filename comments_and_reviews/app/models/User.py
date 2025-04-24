class User:
    id: int
    name: str
    banned: bool
    avatar: str | None

    def __init__(
        self, id: int, name: str, banned: bool, avatar: str | None = None
    ):
        self.id = id
        self.name = name
        self.banned = banned
        self.avatar = avatar

    def demote_to_buyer(self) -> "User":
        return Buyer(self.id, self.name, self.banned, self.avatar)

    def isBanned(self) -> bool:
        return self.banned


class Moderator(User):
    def ban(self, user: User) -> User:
        user.banned = True
        return user

    def unban(self, user: User) -> User:
        user.banned = False
        return user


class Admin(Moderator):
    def ban(self, user: User):
        if isinstance(user, Moderator):
            user = user.demote_to_buyer()
        return super().ban(user)


class Operator(Moderator):
    def ban(self, user: User):
        if not isinstance(user, Moderator):
            return super().ban(user)
        else:
            return user


class Seller(User):
    pass


class Buyer(User):
    pass
