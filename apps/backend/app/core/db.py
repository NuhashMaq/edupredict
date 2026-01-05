from __future__ import annotations

from functools import lru_cache

from pathlib import Path

from urllib.parse import urlparse

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.settings import get_settings


def _backend_root() -> Path:
    # apps/backend/app/core/db.py -> parents[2] == apps/backend
    return Path(__file__).resolve().parents[2]


def _normalize_database_url(database_url: str) -> str:
    """Normalize local SQLite URLs so they work regardless of process CWD.

    In local dev we use:
        sqlite+aiosqlite:///./edupredict.db
    which is CWD-relative. If you start uvicorn from a different directory,
    you'll silently get a different database file (and logins appear to "break").
    """

    try:
        parsed = urlparse(database_url)
    except Exception:
        return database_url

    if not parsed.scheme.startswith("sqlite"):
        return database_url

    # urlparse yields paths like:
    #   /./edupredict.db  (relative)
    #   /C:/path/to/db    (absolute Windows)
    p = parsed.path or ""
    if p.startswith("/./") or p.startswith("/../"):
        rel = p.lstrip("/")  # './edupredict.db'
        abs_path = (_backend_root() / rel).resolve().as_posix()
        return f"{parsed.scheme}:///{abs_path}"

    return database_url


@lru_cache
def get_engine() -> AsyncEngine:
    settings = get_settings()
    return create_async_engine(
        _normalize_database_url(settings.database_url),
        pool_pre_ping=True,
        future=True,
    )


@lru_cache
def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=get_engine(), expire_on_commit=False, autoflush=False)


async def get_db_session() -> AsyncSession:
    SessionLocal = get_sessionmaker()
    async with SessionLocal() as session:
        yield session
