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
async def test_admin_can_train_model_from_records(client, bootstrap_token, tmp_path, monkeypatch):
    # isolate registry
    monkeypatch.setenv("MODEL_REGISTRY_PATH", str(tmp_path / "registry"))

    # bootstrap admin
    res = await client.post(
        "/bootstrap/admin",
        json={
            "bootstrap_token": bootstrap_token,
            "email": "admin-train@example.com",
            "password": "SuperSecure123",
            "full_name": "Admin Train",
        },
    )
    assert res.status_code == 201

    admin_tokens = await _login(client, email="admin-train@example.com", password="SuperSecure123")
    admin_auth = {"Authorization": f"Bearer {admin_tokens['access_token']}"}

    # create a teacher + student
    res = await client.post(
        "/admin/users",
        headers=admin_auth,
        json={
            "email": "teacher-train@example.com",
            "full_name": "Teacher Train",
            "role": "teacher",
            "password": "SuperSecure123",
        },
    )
    assert res.status_code == 201

    res = await client.post(
        "/admin/users",
        headers=admin_auth,
        json={
            "email": "student-train@example.com",
            "full_name": "Student Train",
            "role": "student",
            "password": "SuperSecure123",
        },
    )
    assert res.status_code == 201
    student_id = res.json()["id"]

    teacher_tokens = await _login(client, email="teacher-train@example.com", password="SuperSecure123")
    teacher_auth = {"Authorization": f"Bearer {teacher_tokens['access_token']}"}

    # create enough records for training (min_rows default=20)
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

    # train
    res = await client.post("/ml/train", headers=admin_auth, json={"notes": "endpoint-test"})
    assert res.status_code == 200
    body = res.json()
    assert body["trained"] is True
    assert body["model"]["model_version"]
    assert body["model"]["metrics"]

    # model info should now be available
    res = await client.get("/ml/model", headers=admin_auth)
    assert res.status_code == 200
    info = res.json()
    assert info["notes"] == "endpoint-test"
