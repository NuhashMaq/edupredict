from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class AcademicRecordBase(BaseModel):
    attendance_pct: int = Field(ge=0, le=100)
    assignments_pct: int = Field(ge=0, le=100)
    quizzes_pct: int = Field(ge=0, le=100)
    exams_pct: int = Field(ge=0, le=100)
    gpa: float = Field(ge=0.0, le=4.0)
    term: str | None = Field(default=None, max_length=64)


class AcademicRecordCreate(AcademicRecordBase):
    student_user_id: uuid.UUID


class AcademicRecordUpdate(BaseModel):
    attendance_pct: int | None = Field(default=None, ge=0, le=100)
    assignments_pct: int | None = Field(default=None, ge=0, le=100)
    quizzes_pct: int | None = Field(default=None, ge=0, le=100)
    exams_pct: int | None = Field(default=None, ge=0, le=100)
    gpa: float | None = Field(default=None, ge=0.0, le=4.0)
    term: str | None = Field(default=None, max_length=64)


class AcademicRecordPublic(AcademicRecordBase):
    id: uuid.UUID
    student_user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class AcademicRecordList(BaseModel):
    items: list[AcademicRecordPublic]
    total: int


class AcademicImportRowError(BaseModel):
    row: int = Field(ge=1, description="1-based row number in the CSV including header as row 1")
    message: str
    raw: dict[str, str] | None = None


class AcademicImportResponse(BaseModel):
    dry_run: bool
    total_rows: int = Field(ge=0)
    created: int = Field(ge=0)
    errors: list[AcademicImportRowError] = []
