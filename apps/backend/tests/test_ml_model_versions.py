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
async def test_list_and_promote_models(client, bootstrap_token):
    # bootstrap admin
    res = await client.post(
        "/bootstrap/admin",
        json={
            "bootstrap_token": bootstrap_token,
            "email": "admin-versions@example.com",
            "password": "SuperSecure123",
            "full_name": "Admin Versions",
        },
    )
    assert res.status_code == 201

    admin_tokens = await _login(client, email="admin-versions@example.com", password="SuperSecure123")
    admin_auth = {"Authorization": f"Bearer {admin_tokens['access_token']}"}

    # create a teacher + student
    res = await client.post(
        "/admin/users",
        headers=admin_auth,
        json={
            "email": "teacher-versions@example.com",
            "full_name": "Teacher Versions",
            "role": "teacher",
            "password": "SuperSecure123",
        },
    )
    assert res.status_code == 201

    res = await client.post(
        "/admin/users",
        headers=admin_auth,
        json={
            "email": "student-versions@example.com",
            "full_name": "Student Versions",
            "role": "student",
            "password": "SuperSecure123",
        },
    )
    assert res.status_code == 201
    student_id = res.json()["id"]

    teacher_tokens = await _login(client, email="teacher-versions@example.com", password="SuperSecure123")
    teacher_auth = {"Authorization": f"Bearer {teacher_tokens['access_token']}"}

    # create enough records for training
    for i in range(25):
        res = await client.post(
            "/academics",
            headers=teacher_auth,
            json={
                "student_user_id": student_id,
                "attendance_pct": 60 + (i % 40),
                "assignments_pct": 55 + (i % 45),
                "quizzes_pct": 50 + (i % 50),
                "exams_pct": 45 + (i % 55),
                "gpa": 1.0 + ((i % 30) / 10.0),
                "term": "2026-Spring",
            },
        )
        assert res.status_code == 201

    # train twice to produce two versions
    res = await client.post("/ml/train", headers=admin_auth, json={"notes": "first-train", "min_rows": 20})
    assert res.status_code == 200
    v1 = res.json()["model"]["model_version"]

    res = await client.post("/ml/train", headers=admin_auth, json={"notes": "second-train", "min_rows": 20})
    assert res.status_code == 200
    v2 = res.json()["model"]["model_version"]

    assert v1 != v2

    # listing should include both and latest should be the second train
    res = await client.get("/ml/models?limit=50", headers=admin_auth)
    assert res.status_code == 200
    data = res.json()

    assert data["latest_version"] == v2
    versions = [m["model_version"] for m in data["items"]]
    assert v1 in versions and v2 in versions

    # promote v1 and ensure /ml/model follows
    res = await client.post(f"/ml/models/{v1}/promote", headers=admin_auth)
    assert res.status_code == 200
    assert res.json()["latest_version"] == v1

    res = await client.get("/ml/model", headers=admin_auth)
    assert res.status_code == 200
    assert res.json()["model_version"] == v1
