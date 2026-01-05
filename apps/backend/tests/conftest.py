from __future__ import annotations

import os
import shutil
import tempfile
from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.db import get_db_session
from app.main import create_app
from app.models.base import Base
from app.core.settings import get_settings


@pytest.fixture(scope="session")
def bootstrap_token() -> str:
    return "test-bootstrap-token-12345"


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    # httpx uses anyio under the hood.
    return "asyncio"


@pytest.fixture(scope="session")
async def engine(tmp_path_factory) -> AsyncIterator[AsyncEngine]:
    # CI-friendly default: SQLite. Postgres can be used in integration tests later.
    db_path = tmp_path_factory.mktemp("db") / "test.db"
    url = f"sqlite+aiosqlite:///{db_path}"

    eng = create_async_engine(url, future=True)
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield eng
    finally:
        await eng.dispose()


@pytest.fixture()
async def session(engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    # Keep tests isolated: recreate tables per test.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    SessionLocal = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)
    async with SessionLocal() as s:
        yield s


@pytest.fixture()
async def client(session: AsyncSession) -> AsyncIterator[AsyncClient]:
    # Ensure settings are deterministic for test runs.
    os.environ["ALLOW_ADMIN_BOOTSTRAP"] = "true"
    os.environ["ADMIN_BOOTSTRAP_TOKEN"] = "test-bootstrap-token-12345"

    # Isolate ML registry writes per test.
    ml_registry_dir = tempfile.mkdtemp(prefix="edupredict-ml-registry-")
    os.environ["MODEL_REGISTRY_PATH"] = ml_registry_dir
    get_settings.cache_clear()

    app = create_app()

    async def _override_get_db_session():
        yield session

    app.dependency_overrides[get_db_session] = _override_get_db_session

    transport = ASGITransport(app=app)
    try:
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac
    finally:
        shutil.rmtree(ml_registry_dir, ignore_errors=True)
