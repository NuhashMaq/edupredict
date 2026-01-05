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
async def test_users_list_forbidden_for_student(client):
    # Student registers and logs in
    res = await client.post(
        "/auth/register",
        json={"email": "s@example.com", "password": "SuperSecure123", "full_name": "Stu"},
    )
    assert res.status_code == 201
    tokens = await _login(client, email="s@example.com", password="SuperSecure123")

    res = await client.get("/users", headers={"Authorization": f"Bearer {tokens['access_token']}"})
    assert res.status_code == 403


@pytest.mark.anyio
async def test_users_list_teacher_sees_students_only(client, bootstrap_token):
    # Bootstrap admin
    res = await client.post(
        "/bootstrap/admin",
        json={
            "bootstrap_token": bootstrap_token,
            "email": "admin@example.com",
            "password": "SuperSecure123",
            "full_name": "Admin",
        },
    )
    assert res.status_code == 201

    admin_tokens = await _login(client, email="admin@example.com", password="SuperSecure123")
    admin_auth = {"Authorization": f"Bearer {admin_tokens['access_token']}"}

    # Create teacher + student via admin
    res = await client.post(
        "/admin/users",
        headers=admin_auth,
        json={
            "email": "teacher@example.com",
            "full_name": "Teacher",
            "role": "teacher",
            "password": "SuperSecure123",
        },
    )
    assert res.status_code == 201

    res = await client.post(
        "/admin/users",
        headers=admin_auth,
        json={
            "email": "student@example.com",
            "full_name": "Student",
            "role": "student",
            "password": "SuperSecure123",
        },
    )
    assert res.status_code == 201

    teacher_tokens = await _login(client, email="teacher@example.com", password="SuperSecure123")
    teacher_auth = {"Authorization": f"Bearer {teacher_tokens['access_token']}"}

    # Teacher requests role=admin but should still only get students
    res = await client.get("/users?role=admin", headers=teacher_auth)
    assert res.status_code == 200
    body = res.json()

    assert body["total"] >= 1
    assert all(u["role"] == "student" for u in body["items"])


@pytest.mark.anyio
async def test_users_list_admin_filters_by_role(client, bootstrap_token):
    # Bootstrap admin
    res = await client.post(
        "/bootstrap/admin",
        json={
            "bootstrap_token": bootstrap_token,
            "email": "admin2@example.com",
            "password": "SuperSecure123",
            "full_name": "Admin2",
        },
    )
    assert res.status_code == 201

    admin_tokens = await _login(client, email="admin2@example.com", password="SuperSecure123")
    admin_auth = {"Authorization": f"Bearer {admin_tokens['access_token']}"}

    # Create a teacher
    res = await client.post(
        "/admin/users",
        headers=admin_auth,
        json={
            "email": "teacher2@example.com",
            "full_name": "Teacher2",
            "role": "teacher",
            "password": "SuperSecure123",
        },
    )
    assert res.status_code == 201

    res = await client.get("/users?role=teacher", headers=admin_auth)
    assert res.status_code == 200
    body = res.json()

    assert body["total"] >= 1
    assert any(u["email"] == "teacher2@example.com" for u in body["items"])
    assert all(u["role"] == "teacher" for u in body["items"])
