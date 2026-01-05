from __future__ import annotations

import csv
import io
import secrets
import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db_session
from app.deps.auth import get_current_user, require_roles
from app.models.academic_record import AcademicRecord
from app.models.user import User, UserRole
from app.schemas.academic import (
    AcademicRecordCreate,
    AcademicRecordList,
    AcademicRecordPublic,
    AcademicImportResponse,
    AcademicImportRowError,
    AcademicRecordUpdate,
)
from app.services.academics import AcademicsService
from app.services.users import UsersService

router = APIRouter(prefix="/academics", tags=["academics"])


def _to_public(r: AcademicRecord) -> AcademicRecordPublic:
    return AcademicRecordPublic.model_validate(r, from_attributes=True)


def _parse_int(v: str, *, field: str) -> int:
    try:
        return int(v)
    except Exception as e:
        raise ValueError(f"{field} must be an integer") from e


def _parse_float(v: str, *, field: str) -> float:
    try:
        return float(v)
    except Exception as e:
        raise ValueError(f"{field} must be a number") from e


def _require(row: dict[str, str], key: str) -> str:
    v = (row.get(key) or "").strip()
    if not v:
        raise ValueError(f"Missing required column '{key}'")
    return v


def _opt(row: dict[str, str], key: str) -> str | None:
    v = (row.get(key) or "").strip()
    return v or None


def _has_fields(fieldnames: list[str] | None, required: set[str]) -> bool:
    if not fieldnames:
        return False
    fields = {f.strip() for f in fieldnames if f}
    return required.issubset(fields)


def _normalize_term(row: dict[str, str]) -> str | None:
    # RUET datasets often use "semester" like 1-1, 1-2, ...
    return _opt(row, "term") or _opt(row, "semester")


async def _get_or_create_student_by_email(
    users: UsersService,
    *,
    email: str,
    allow_create: bool,
) -> User | None:
    student = await users.get_by_email(email)
    if student:
        return student

    if not allow_create:
        return None

    # Create a non-interactive demo student if missing.
    # Password is random and not surfaced; admin can reset later if needed.
    password = secrets.token_urlsafe(18)
    return await users.create_user(email=email, full_name="", role=UserRole.student, password=password)


@router.get("/me", response_model=AcademicRecordList)
async def list_my_records(
    term: str | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_db_session),
    user: User = Depends(require_roles(UserRole.student)),
) -> AcademicRecordList:
    items, total = await AcademicsService(session).list(
        student_user_id=user.id,
        term=term,
        limit=limit,
        offset=offset,
    )
    return AcademicRecordList(items=[_to_public(i) for i in items], total=total)


@router.get("", response_model=AcademicRecordList)
async def list_records(
    student_user_id: uuid.UUID | None = None,
    term: str | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> AcademicRecordList:
    # Teachers + Admins can list records. Students can only list their own.
    if user.role == UserRole.student:
        if student_user_id is not None and student_user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        student_user_id = user.id
    elif user.role not in (UserRole.teacher, UserRole.admin):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    items, total = await AcademicsService(session).list(
        student_user_id=student_user_id,
        term=term,
        limit=limit,
        offset=offset,
    )
    return AcademicRecordList(items=[_to_public(i) for i in items], total=total)


@router.post(
    "",
    response_model=AcademicRecordPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(UserRole.teacher, UserRole.admin))],
)
async def create_record(
    body: AcademicRecordCreate,
    session: AsyncSession = Depends(get_db_session),
) -> AcademicRecordPublic:
    student = await UsersService(session).get_by_id(body.student_user_id)
    if not student or not student.is_active or student.role != UserRole.student:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid student_user_id")

    record = AcademicRecord(**body.model_dump())
    created = await AcademicsService(session).create(record)
    return _to_public(created)


@router.patch(
    "/{record_id}",
    response_model=AcademicRecordPublic,
    dependencies=[Depends(require_roles(UserRole.teacher, UserRole.admin))],
)
async def update_record(
    record_id: uuid.UUID,
    body: AcademicRecordUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> AcademicRecordPublic:
    svc = AcademicsService(session)
    record = svc.forbid_if_none(await svc.get(record_id))
    patch = {k: v for k, v in body.model_dump().items() if v is not None}
    updated = await svc.update(record, patch)
    return _to_public(updated)


@router.delete(
    "/{record_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(UserRole.admin))],
)
async def delete_record(
    record_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
) -> None:
    svc = AcademicsService(session)
    record = svc.forbid_if_none(await svc.get(record_id))
    await svc.delete(record)


@router.post(
    "/import",
    response_model=AcademicImportResponse,
    dependencies=[Depends(require_roles(UserRole.teacher, UserRole.admin))],
)
async def import_records_csv(
    file: UploadFile = File(...),
    dry_run: bool = Form(default=False),
    session: AsyncSession = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> AcademicImportResponse:
    """Bulk import academic records from a CSV file.

    Supported formats:

    1) Summary format (one row per student per term):
       - student_user_id OR student_email
       - attendance_pct, assignments_pct, quizzes_pct, exams_pct, gpa
       - term (optional)

    2) RUET course-marks format (multiple rows per student per term, aggregated server-side):
       - student_email (or student_user_id)
       - term OR semester
       - credits, grade_point_4
       - attendance_10, assignments_10, ct_20 (optional), final_60

    Notes:
    - If importing as an admin and a referenced student_email doesn't exist yet, a student user is auto-created.
    """

    raw = await file.read()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        # Fallback common on Windows exports
        text = raw.decode("latin-1")

    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CSV missing header row")

    allow_autocreate_students = user.role == UserRole.admin

    # Detect format from headers
    is_summary = _has_fields(
        reader.fieldnames,
        {"attendance_pct", "assignments_pct", "quizzes_pct", "exams_pct", "gpa"},
    )
    is_ruet_course = _has_fields(
        reader.fieldnames,
        {"credits", "grade_point_4", "attendance_10", "assignments_10", "final_60"},
    )

    errors: list[AcademicImportRowError] = []
    records: list[AcademicRecord] = []
    users = UsersService(session)

    row_num = 1  # header row

    if is_ruet_course and not is_summary:
        # RUET course-marks import: aggregate multiple rows into one AcademicRecord per student+term.
        # We aggregate using credit-weighted averages.
        groups: dict[tuple[str, str], dict[str, float]] = {}
        group_raw_first: dict[tuple[str, str], dict[str, str]] = {}

        for row in reader:
            row_num += 1
            try:
                student_email = _opt(row, "student_email")
                if not student_email:
                    raise ValueError("Missing required column 'student_email'")

                term = _normalize_term(row)
                if not term:
                    raise ValueError("Missing required column 'term' (or 'semester')")

                credits = _parse_float(_require(row, "credits"), field="credits")
                if credits <= 0:
                    raise ValueError("credits must be > 0")

                gp = _parse_float(_require(row, "grade_point_4"), field="grade_point_4")
                if gp < 0.0 or gp > 4.0:
                    raise ValueError("grade_point_4 must be 0.0-4.0")

                a10 = _parse_float(_require(row, "attendance_10"), field="attendance_10")
                as10 = _parse_float(_require(row, "assignments_10"), field="assignments_10")
                ct20_raw = _opt(row, "ct_20")
                ct20 = _parse_float(ct20_raw, field="ct_20") if ct20_raw is not None else 0.0
                f60 = _parse_float(_require(row, "final_60"), field="final_60")

                # Convert component marks to 0-100 signals expected by the ML model.
                attendance_pct = (a10 / 10.0) * 100.0
                assignments_pct = (as10 / 10.0) * 100.0
                quizzes_pct = (ct20 / 20.0) * 100.0
                exams_pct = (f60 / 60.0) * 100.0

                for name, val in (
                    ("attendance_pct", attendance_pct),
                    ("assignments_pct", assignments_pct),
                    ("quizzes_pct", quizzes_pct),
                    ("exams_pct", exams_pct),
                ):
                    if val < 0 or val > 100:
                        raise ValueError(f"{name} derived from marks is out of range")

                key = (student_email.lower().strip(), term)
                if key not in groups:
                    groups[key] = {
                        "w": 0.0,
                        "attendance": 0.0,
                        "assignments": 0.0,
                        "quizzes": 0.0,
                        "exams": 0.0,
                        "gpa": 0.0,
                    }
                    group_raw_first[key] = {k: (v if v is not None else "") for k, v in row.items()}

                g = groups[key]
                g["w"] += credits
                g["attendance"] += attendance_pct * credits
                g["assignments"] += assignments_pct * credits
                g["quizzes"] += quizzes_pct * credits
                g["exams"] += exams_pct * credits
                g["gpa"] += gp * credits
            except Exception as e:
                errors.append(
                    AcademicImportRowError(
                        row=row_num,
                        message=str(e),
                        raw={k: (v if v is not None else "") for k, v in row.items()},
                    )
                )

        for (student_email, term), agg in groups.items():
            try:
                student = await _get_or_create_student_by_email(
                    users,
                    email=student_email,
                    allow_create=allow_autocreate_students,
                )
                if not student or not student.is_active or student.role != UserRole.student:
                    raise ValueError("Invalid student reference")

                w = agg["w"]
                if w <= 0:
                    raise ValueError("No credit weight found for term")

                attendance_pct = int(round(agg["attendance"] / w))
                assignments_pct = int(round(agg["assignments"] / w))
                quizzes_pct = int(round(agg["quizzes"] / w))
                exams_pct = int(round(agg["exams"] / w))
                gpa = float(agg["gpa"] / w)

                # Clamp for safety
                attendance_pct = max(0, min(100, attendance_pct))
                assignments_pct = max(0, min(100, assignments_pct))
                quizzes_pct = max(0, min(100, quizzes_pct))
                exams_pct = max(0, min(100, exams_pct))
                gpa = max(0.0, min(4.0, gpa))

                records.append(
                    AcademicRecord(
                        student_user_id=student.id,
                        attendance_pct=attendance_pct,
                        assignments_pct=assignments_pct,
                        quizzes_pct=quizzes_pct,
                        exams_pct=exams_pct,
                        gpa=gpa,
                        term=term,
                    )
                )
            except Exception as e:
                errors.append(
                    AcademicImportRowError(
                        row=1,
                        message=f"{student_email} / {term}: {e}",
                        raw=group_raw_first.get((student_email, term)),
                    )
                )
    else:
        # Summary import (existing format)
        for row in reader:
            row_num += 1
            try:
                student_user_id = _opt(row, "student_user_id")
                student_email = _opt(row, "student_email")

                student: User | None = None
                if student_user_id:
                    student = await users.get_by_id(student_user_id)
                elif student_email:
                    student = await _get_or_create_student_by_email(
                        users,
                        email=student_email,
                        allow_create=allow_autocreate_students,
                    )
                else:
                    raise ValueError("Provide student_user_id or student_email")

                if not student or not student.is_active or student.role != UserRole.student:
                    raise ValueError("Invalid student reference")

                attendance_pct = _parse_int(_require(row, "attendance_pct"), field="attendance_pct")
                assignments_pct = _parse_int(_require(row, "assignments_pct"), field="assignments_pct")
                quizzes_pct = _parse_int(_require(row, "quizzes_pct"), field="quizzes_pct")
                exams_pct = _parse_int(_require(row, "exams_pct"), field="exams_pct")
                gpa = _parse_float(_require(row, "gpa"), field="gpa")
                term = _normalize_term(row)

                # Range validation (mirrors Pydantic/model constraints)
                for name, val in (
                    ("attendance_pct", attendance_pct),
                    ("assignments_pct", assignments_pct),
                    ("quizzes_pct", quizzes_pct),
                    ("exams_pct", exams_pct),
                ):
                    if val < 0 or val > 100:
                        raise ValueError(f"{name} must be 0-100")
                if gpa < 0.0 or gpa > 4.0:
                    raise ValueError("gpa must be 0.0-4.0")

                records.append(
                    AcademicRecord(
                        student_user_id=student.id,
                        attendance_pct=attendance_pct,
                        assignments_pct=assignments_pct,
                        quizzes_pct=quizzes_pct,
                        exams_pct=exams_pct,
                        gpa=gpa,
                        term=term,
                    )
                )
            except Exception as e:
                errors.append(
                    AcademicImportRowError(
                        row=row_num,
                        message=str(e),
                        raw={k: (v if v is not None else "") for k, v in row.items()},
                    )
                )

    if dry_run:
        return AcademicImportResponse(dry_run=True, total_rows=max(0, row_num - 1), created=len(records), errors=errors)

    if records:
        session.add_all(records)
        await session.commit()

    return AcademicImportResponse(dry_run=False, total_rows=max(0, row_num - 1), created=len(records), errors=errors)
