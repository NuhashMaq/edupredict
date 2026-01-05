from __future__ import annotations

import io

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
async def test_academics_import_creates_records(client, bootstrap_token):
    # Bootstrap admin
    res = await client.post(
        "/bootstrap/admin",
        json={
            "bootstrap_token": bootstrap_token,
            "email": "admin-import@example.com",
            "password": "SuperSecure123",
            "full_name": "Admin Import",
        },
    )
    assert res.status_code == 201

    admin_tokens = await _login(client, email="admin-import@example.com", password="SuperSecure123")
    admin_auth = {"Authorization": f"Bearer {admin_tokens['access_token']}"}

    # Create teacher + student
    res = await client.post(
        "/admin/users",
        headers=admin_auth,
        json={
            "email": "teacher-import@example.com",
            "full_name": "Teacher Import",
            "role": "teacher",
            "password": "SuperSecure123",
        },
    )
    assert res.status_code == 201

    res = await client.post(
        "/admin/users",
        headers=admin_auth,
        json={
            "email": "student-import@example.com",
            "full_name": "Student Import",
            "role": "student",
            "password": "SuperSecure123",
        },
    )
    assert res.status_code == 201
    student_id = res.json()["id"]

    teacher_tokens = await _login(client, email="teacher-import@example.com", password="SuperSecure123")
    teacher_auth = {"Authorization": f"Bearer {teacher_tokens['access_token']}"}

    csv_text = (
        "student_user_id,attendance_pct,assignments_pct,quizzes_pct,exams_pct,gpa,term\n"
        f"{student_id},95,88,90,84,3.6,Fall 2025\n"
    )

    files = {"file": ("import.csv", io.BytesIO(csv_text.encode("utf-8")), "text/csv")}
    data = {"dry_run": "false"}

    res = await client.post("/academics/import", headers=teacher_auth, files=files, data=data)
    assert res.status_code == 200
    body = res.json()
    assert body["dry_run"] is False
    assert body["created"] == 1
    assert body["errors"] == []

    # Record should be visible
    res = await client.get(f"/academics?student_user_id={student_id}", headers=teacher_auth)
    assert res.status_code == 200
    items = res.json()["items"]
    assert len(items) == 1
    assert items[0]["gpa"] == 3.6


@pytest.mark.anyio
async def test_academics_import_dry_run_and_errors(client, bootstrap_token):
    # Bootstrap admin
    res = await client.post(
        "/bootstrap/admin",
        json={
            "bootstrap_token": bootstrap_token,
            "email": "admin-import2@example.com",
            "password": "SuperSecure123",
            "full_name": "Admin Import2",
        },
    )
    assert res.status_code == 201

    admin_tokens = await _login(client, email="admin-import2@example.com", password="SuperSecure123")
    admin_auth = {"Authorization": f"Bearer {admin_tokens['access_token']}"}

    # Create teacher + student
    res = await client.post(
        "/admin/users",
        headers=admin_auth,
        json={
            "email": "teacher-import2@example.com",
            "full_name": "Teacher Import2",
            "role": "teacher",
            "password": "SuperSecure123",
        },
    )
    assert res.status_code == 201

    res = await client.post(
        "/admin/users",
        headers=admin_auth,
        json={
            "email": "student-import2@example.com",
            "full_name": "Student Import2",
            "role": "student",
            "password": "SuperSecure123",
        },
    )
    assert res.status_code == 201
    student_id = res.json()["id"]

    teacher_tokens = await _login(client, email="teacher-import2@example.com", password="SuperSecure123")
    teacher_auth = {"Authorization": f"Bearer {teacher_tokens['access_token']}"}

    # One valid row + one invalid row (gpa out of range)
    csv_text = (
        "student_user_id,attendance_pct,assignments_pct,quizzes_pct,exams_pct,gpa,term\n"
        f"{student_id},80,80,80,80,3.2,Spring 2026\n"
        f"{student_id},80,80,80,80,6.2,Spring 2026\n"
    )

    files = {"file": ("import.csv", io.BytesIO(csv_text.encode("utf-8")), "text/csv")}
    data = {"dry_run": "true"}

    res = await client.post("/academics/import", headers=teacher_auth, files=files, data=data)
    assert res.status_code == 200
    body = res.json()

    assert body["dry_run"] is True
    assert body["created"] == 1
    assert len(body["errors"]) == 1

    # Dry-run should not create records
    res = await client.get(f"/academics?student_user_id={student_id}", headers=teacher_auth)
    assert res.status_code == 200
    assert res.json()["items"] == []
