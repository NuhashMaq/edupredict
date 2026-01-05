from __future__ import annotations

from datetime import datetime
from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_jwt,
    decode_jwt,
    hash_refresh_token_token,
    utcnow,
    verify_password,
)
from app.core.settings import get_settings
from app.models.refresh_token import RefreshToken
from app.models.user import User, UserRole
from app.services.users import UsersService


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UsersService(session)

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.users.get_by_email(email)
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return user

    async def issue_token_pair(self, user: User) -> tuple[str, str]:
        settings = get_settings()

        access = create_jwt(
            subject=str(user.id),
            token_type="access",
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
            extra={"role": user.role.value},
        )

        refresh = create_jwt(
            subject=str(user.id),
            token_type="refresh",
            expires_delta=timedelta(days=settings.refresh_token_expire_days),
            extra={"role": user.role.value},
        )

        payload = decode_jwt(refresh)
        jti = str(payload["jti"])
        exp_ts = int(payload["exp"])

        rt = RefreshToken(
            user_id=user.id,
            jti=jti,
            token_hash=hash_refresh_token_token(refresh),
            expires_at=datetime.fromtimestamp(exp_ts, tz=utcnow().tzinfo),
        )
        self.session.add(rt)
        await self.session.commit()

        return access, refresh

    async def refresh(self, refresh_token: str) -> tuple[str, str]:
        try:
            payload = decode_jwt(refresh_token)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user_id = payload.get("sub")
        jti = payload.get("jti")

        res = await self.session.execute(select(RefreshToken).where(RefreshToken.jti == str(jti)))
        row = res.scalar_one_or_none()
        if not row or row.revoked_at is not None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked")

        if row.token_hash != hash_refresh_token_token(refresh_token):
            # Token replay / DB mismatch.
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        # Rotate: revoke the old refresh token and issue a new pair.
        row.revoked_at = utcnow()
        await self.session.commit()

        user = await self.users.get_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        return await self.issue_token_pair(user)

    async def logout(self, refresh_token: str) -> None:
        try:
            payload = decode_jwt(refresh_token)
        except ValueError:
            # Logout should be idempotent.
            return
        if payload.get("type") != "refresh":
            return

        jti = str(payload.get("jti"))
        res = await self.session.execute(select(RefreshToken).where(RefreshToken.jti == jti))
        row = res.scalar_one_or_none()
        if row and row.revoked_at is None:
            row.revoked_at = utcnow()
            await self.session.commit()


def coerce_role(role: str) -> UserRole:
    try:
        return UserRole(role)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role") from e
