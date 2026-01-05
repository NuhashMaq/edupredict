from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Literal

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.settings import get_settings

# bcrypt has a 72-byte effective limit and some bcrypt backends on Windows may
# raise errors during passlib's backend self-checks.
# pbkdf2_sha256 is a solid, widely-supported default for app passwords.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

TokenType = Literal["access", "refresh"]


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def _base_claims() -> dict[str, Any]:
    settings = get_settings()
    return {
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
    }


def create_jwt(*, subject: str, token_type: TokenType, expires_delta: timedelta, extra: dict[str, Any]) -> str:
    settings = get_settings()
    now = utcnow()
    jti = str(uuid.uuid4())

    payload: dict[str, Any] = {
        **_base_claims(),
        "sub": subject,
        "type": token_type,
        "jti": jti,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
        **extra,
    }

    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def decode_jwt(token: str) -> dict[str, Any]:
    settings = get_settings()
    try:
        return jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=["HS256"],
            audience=settings.jwt_audience,
            issuer=settings.jwt_issuer,
            options={"require": ["exp", "iat", "sub", "type", "jti"]},
        )
    except JWTError as e:
        raise ValueError("Invalid token") from e


def hash_refresh_token_token(token: str) -> str:
    # DB-safe hash: we never store refresh tokens in plaintext.
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
