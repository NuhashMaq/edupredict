from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Float, Integer, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AcademicRecord(Base):
    """A normalized snapshot of a student's academic signals.

    This is intentionally *tabular* and model-friendly (good for ML pipelines) while
    still being human-readable for dashboards.
    """

    __tablename__ = "academic_records"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)

    student_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )

    # Percentage-based signals (0-100)
    attendance_pct: Mapped[int] = mapped_column(Integer)
    assignments_pct: Mapped[int] = mapped_column(Integer)
    quizzes_pct: Mapped[int] = mapped_column(Integer)
    exams_pct: Mapped[int] = mapped_column(Integer)

    # GPA on 0.0 - 4.0 scale (float for compatibility with common SIS exports)
    gpa: Mapped[float] = mapped_column(Float)

    # Optional metadata for longitudinal analysis.
    term: Mapped[str | None] = mapped_column(default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        CheckConstraint("attendance_pct >= 0 AND attendance_pct <= 100", name="ck_attendance_pct"),
        CheckConstraint("assignments_pct >= 0 AND assignments_pct <= 100", name="ck_assignments_pct"),
        CheckConstraint("quizzes_pct >= 0 AND quizzes_pct <= 100", name="ck_quizzes_pct"),
        CheckConstraint("exams_pct >= 0 AND exams_pct <= 100", name="ck_exams_pct"),
        CheckConstraint("gpa >= 0.0 AND gpa <= 4.0", name="ck_gpa_range"),
    )
