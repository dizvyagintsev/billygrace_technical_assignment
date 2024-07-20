from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    email: str
    displayName: str
    role: str
    photoURL: Optional[str] = None


class LoginResponse(BaseModel):
    accessToken: str
    user: User


class LoginRequest(BaseModel):
    email: str
    password: str
