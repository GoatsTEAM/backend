from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str | None
    avatar: str | None
    banned: bool

    def ban(self) -> "User":
        if self.is_banned():
            raise ValueError("User already banned")
        return self.model_copy(update={"banned": True})

    def unban(self) -> "User":
        if not self.is_banned():
            raise ValueError("User not banned")
        return self.model_copy(update={"banned": False})

    def is_banned(self) -> bool:
        return self.banned
