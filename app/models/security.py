# security/models.py
from pydantic import BaseModel


class AuthenticatedUser(BaseModel):
    user_id: str
    email: str | None = None
    apps: list[str] = []
