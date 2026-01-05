from __future__ import annotations

import pytest


async def _login(client, *, email: str, password: str) -> dict:
    res = await client.post(
        "/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert res.status_code == 200
    return res.json()


@pytest.mark.anyio
async def test_student_forbidden_from_admin_create_user(client):
    await client.post(
        "/auth/register",
        json={"email": "student3@example.com", "password": "SuperSecure123", "full_name": "Cy Student"},
    )
    tokens = await _login(client, email="student3@example.com", password="SuperSecure123")

    res = await client.post(
        "/admin/users",
        json={
            "email": "teacher1@example.com",
            "full_name": "Tess Teacher",
            "role": "teacher",
            "password": "AnotherSuperSecure123",
        },
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )

    assert res.status_code == 403


@pytest.mark.anyio
async def test_bootstrap_admin_then_admin_can_create_user(client):
    # Bootstrap first admin (only allowed when enabled + token matches)
    res = await client.post(
        "/bootstrap/admin",
        json={
            "bootstrap_token": "test-bootstrap-token-12345",
            "email": "admin@example.com",
            "password": "AdminSuperSecure123",
            "full_name": "Ari Admin",
        },
    )
    assert res.status_code == 201

    tokens = await _login(client, email="admin@example.com", password="AdminSuperSecure123")

    res = await client.post(
        "/admin/users",
        json={
            "email": "teacher2@example.com",
            "full_name": "Tori Teacher",
            "role": "teacher",
            "password": "AnotherSuperSecure123",
        },
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )

    assert res.status_code == 201
    body = res.json()
    assert body["email"] == "teacher2@example.com"
    assert body["role"] == "teacher"
