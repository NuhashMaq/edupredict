from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import get_settings
from app.models.user import User, UserRole
from app.services.users import UsersService


class AdminBootstrapService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UsersService(session)

    async def bootstrap_admin(self, *, bootstrap_token: str, email: str, password: str, full_name: str) -> User:
        settings = get_settings()

        if not settings.allow_admin_bootstrap:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bootstrap disabled")

        if not settings.admin_bootstrap_token or bootstrap_token != settings.admin_bootstrap_token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid bootstrap token")

        # Only allow bootstrap if no admin exists yet.
        res = await self.session.execute(select(User).where(User.role == UserRole.admin))
        existing_admin = res.scalar_one_or_none()
        if existing_admin:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Admin already exists")

        return await self.users.create_user(
            email=email,
            full_name=full_name,
            role=UserRole.admin,
            password=password,
        )
