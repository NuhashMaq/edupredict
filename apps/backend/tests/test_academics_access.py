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
async def test_student_can_only_view_own_records(client):
    # student A
    await client.post(
        "/auth/register",
        json={"email": "sa@example.com", "password": "SuperSecure123", "full_name": "Student A"},
    )
    ta = await _login(client, email="sa@example.com", password="SuperSecure123")

    # student B
    await client.post(
        "/auth/register",
        json={"email": "sb@example.com", "password": "SuperSecure123", "full_name": "Student B"},
    )
    tb = await _login(client, email="sb@example.com", password="SuperSecure123")

    # Bootstrap admin to create a teacher
    await client.post(
        "/bootstrap/admin",
        json={
            "bootstrap_token": "test-bootstrap-token-12345",
            "email": "admin2@example.com",
            "password": "AdminSuperSecure123",
            "full_name": "Admin Two",
        },
    )
    admin_tokens = await _login(client, email="admin2@example.com", password="AdminSuperSecure123")

    # Create teacher
    res = await client.post(
        "/admin/users",
        json={
            "email": "teach@example.com",
            "full_name": "Teach",
            "role": "teacher",
            "password": "AnotherSuperSecure123",
        },
        headers={"Authorization": f"Bearer {admin_tokens['access_token']}"},
    )
    assert res.status_code == 201

    teacher_tokens = await _login(client, email="teach@example.com", password="AnotherSuperSecure123")

    # Teacher creates a record for student A (need student id -> via /auth/me)
    me_a = await client.get("/auth/me", headers={"Authorization": f"Bearer {ta['access_token']}"})
    assert me_a.status_code == 200
    student_a_id = me_a.json()["id"]

    res = await client.post(
        "/academics",
        json={
            "student_user_id": student_a_id,
            "attendance_pct": 92,
            "assignments_pct": 86,
            "quizzes_pct": 80,
            "exams_pct": 78,
            "gpa": 3.2,
            "term": "2025-Fall",
        },
        headers={"Authorization": f"Bearer {teacher_tokens['access_token']}"},
    )
    assert res.status_code == 201

    # Student A sees it
    res = await client.get("/academics/me", headers={"Authorization": f"Bearer {ta['access_token']}"})
    assert res.status_code == 200
    assert res.json()["total"] == 1

    # Student B should NOT be able to list student A records by student_user_id
    res = await client.get(
        f"/academics?student_user_id={student_a_id}",
        headers={"Authorization": f"Bearer {tb['access_token']}"},
    )
    assert res.status_code == 403
