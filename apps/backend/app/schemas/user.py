from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UserPublic(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime


class UserCreateAdmin(BaseModel):
    email: EmailStr
    full_name: str = ""
    role: UserRole
    password: str


class UserUpdateAdmin(BaseModel):
    full_name: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class UsersList(BaseModel):
    items: list[UserPublic]
    total: int
