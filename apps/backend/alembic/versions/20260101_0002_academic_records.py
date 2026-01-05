"""add academic records

Revision ID: 20260101_0002
Revises: 20260101_0001
Create Date: 2026-01-01

"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260101_0002"
down_revision = "20260101_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "academic_records",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "student_user_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("attendance_pct", sa.Integer(), nullable=False),
        sa.Column("assignments_pct", sa.Integer(), nullable=False),
        sa.Column("quizzes_pct", sa.Integer(), nullable=False),
        sa.Column("exams_pct", sa.Integer(), nullable=False),
        sa.Column("gpa", sa.Float(), nullable=False),
        sa.Column("term", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("attendance_pct >= 0 AND attendance_pct <= 100", name="ck_attendance_pct"),
        sa.CheckConstraint("assignments_pct >= 0 AND assignments_pct <= 100", name="ck_assignments_pct"),
        sa.CheckConstraint("quizzes_pct >= 0 AND quizzes_pct <= 100", name="ck_quizzes_pct"),
        sa.CheckConstraint("exams_pct >= 0 AND exams_pct <= 100", name="ck_exams_pct"),
        sa.CheckConstraint("gpa >= 0.0 AND gpa <= 4.0", name="ck_gpa_range"),
    )
    op.create_index(
        "ix_academic_records_student_user_id",
        "academic_records",
        ["student_user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_academic_records_student_user_id", table_name="academic_records")
    op.drop_table("academic_records")
