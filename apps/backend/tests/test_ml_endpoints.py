from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
import httpx

from app.core.settings import get_settings
from app.main import create_app
from app.core.db import get_db_session
from app.models.base import Base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


@pytest.mark.anyio
async def test_predict_and_explain_endpoints(tmp_path, monkeypatch):
    # Arrange: temporary registry + train model
    monkeypatch.setenv("MODEL_REGISTRY_PATH", str(tmp_path / "registry"))

    from app.ml.train import train_from_dataframe
    from app.ml.inference import clear_model_cache

    rng = np.random.default_rng(7)
    n = 200
    df = pd.DataFrame(
        {
            "attendance_pct": rng.integers(55, 100, size=n),
            "assignments_pct": rng.integers(40, 100, size=n),
            "quizzes_pct": rng.integers(35, 100, size=n),
            "exams_pct": rng.integers(30, 100, size=n),
            "gpa": rng.random(size=n) * 4.0,
        }
    )
    avg = (df["assignments_pct"] + df["quizzes_pct"] + df["exams_pct"]) / 3.0
    df["at_risk"] = ((df["gpa"] < 2.2) | (df["attendance_pct"] < 78) | (avg < 66)).astype(int)

    train_from_dataframe(df, notes="endpoint-test")
    clear_model_cache()

    # Arrange: isolated test DB + app
    db_path = tmp_path / "db.sqlite"
    engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}", future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    SessionLocal = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)
    async with SessionLocal() as session:
        async def _override_get_db_session():
            yield session

        # ensure settings cache doesn't freeze registry path
        get_settings.cache_clear()

        app = create_app()
        app.dependency_overrides[get_db_session] = _override_get_db_session

        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            # Create student
            res = await client.post(
                "/auth/register",
                json={"email": "mls@example.com", "password": "SuperSecure123", "full_name": "ML Student"},
            )
            assert res.status_code == 201

            # Login
            res = await client.post(
                "/auth/login",
                data={"username": "mls@example.com", "password": "SuperSecure123"},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            assert res.status_code == 200
            tokens = res.json()

            # Student predict with no academic record -> 404
            res = await client.post(
                "/ml/predict",
                json={},
                headers={"Authorization": f"Bearer {tokens['access_token']}"},
            )
            assert res.status_code == 404

            # Bootstrap admin
            monkeypatch.setenv("ALLOW_ADMIN_BOOTSTRAP", "true")
            monkeypatch.setenv("ADMIN_BOOTSTRAP_TOKEN", "test-bootstrap-token-12345")
            get_settings.cache_clear()

            res = await client.post(
                "/bootstrap/admin",
                json={
                    "bootstrap_token": "test-bootstrap-token-12345",
                    "email": "mladmin@example.com",
                    "password": "AdminSuperSecure123",
                    "full_name": "ML Admin",
                },
            )
            assert res.status_code == 201

            # Login admin
            res = await client.post(
                "/auth/login",
                data={"username": "mladmin@example.com", "password": "AdminSuperSecure123"},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            admin_tokens = res.json()

            # Admin explain with features
            res = await client.post(
                "/ml/explain",
                json={
                    "features": {
                        "attendance_pct": 72,
                        "assignments_pct": 60,
                        "quizzes_pct": 58,
                        "exams_pct": 55,
                        "gpa": 2.1,
                    },
                    "top_k": 3,
                },
                headers={"Authorization": f"Bearer {admin_tokens['access_token']}"},
            )
            assert res.status_code == 200
            body = res.json()
            assert body["model_version"]
            assert len(body["factors"]) == 3

    await engine.dispose()
