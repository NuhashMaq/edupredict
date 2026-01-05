from __future__ import annotations

import pytest


@pytest.mark.anyio
async def test_register_login_me(client):
    # Register
    res = await client.post(
        "/auth/register",
        json={"email": "student@example.com", "password": "SuperSecure123", "full_name": "Ada Student"},
    )
    assert res.status_code == 201

    # Login
    res = await client.post(
        "/auth/login",
        data={"username": "student@example.com", "password": "SuperSecure123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert res.status_code == 200
    tokens = res.json()
    assert "access_token" in tokens and "refresh_token" in tokens

    # Me
    res = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["email"] == "student@example.com"
    assert body["role"] == "student"


@pytest.mark.anyio
async def test_refresh_rotation_and_logout(client):
    await client.post(
        "/auth/register",
        json={"email": "student2@example.com", "password": "SuperSecure123", "full_name": "Bea Student"},
    )
    res = await client.post(
        "/auth/login",
        data={"username": "student2@example.com", "password": "SuperSecure123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    tokens1 = res.json()

    # Refresh => rotates refresh token
    res = await client.post("/auth/refresh", json={"refresh_token": tokens1["refresh_token"]})
    assert res.status_code == 200
    tokens2 = res.json()
    assert tokens2["refresh_token"] != tokens1["refresh_token"]

    # Old refresh token should now be revoked
    res = await client.post("/auth/refresh", json={"refresh_token": tokens1["refresh_token"]})
    assert res.status_code in (401, 403)

    # Logout revokes refresh token
    res = await client.post("/auth/logout", json={"refresh_token": tokens2["refresh_token"]})
    assert res.status_code == 204

    res = await client.post("/auth/refresh", json={"refresh_token": tokens2["refresh_token"]})
    assert res.status_code in (401, 403)
