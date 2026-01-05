from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HumanFeature:
    key: str
    label: str
    unit: str | None = None
    guidance: str | None = None


HUMAN_FEATURES: dict[str, HumanFeature] = {
    "attendance_pct": HumanFeature(
        key="attendance_pct",
        label="Attendance",
        unit="%",
        guidance="Lower attendance often correlates with missed instruction time.",
    ),
    "assignments_pct": HumanFeature(
        key="assignments_pct",
        label="Assignments",
        unit="%",
        guidance="Consistent assignment performance indicates engagement and practice.",
    ),
    "quizzes_pct": HumanFeature(
        key="quizzes_pct",
        label="Quizzes",
        unit="%",
        guidance="Quiz scores can reveal short-term retention and knowledge gaps.",
    ),
    "exams_pct": HumanFeature(
        key="exams_pct",
        label="Exams",
        unit="%",
        guidance="Exam performance is a strong proxy for mastery under pressure.",
    ),
    "gpa": HumanFeature(
        key="gpa",
        label="GPA",
        unit="/4.0",
        guidance="GPA summarizes longitudinal performance across subjects.",
    ),
    "grade_ordinal": HumanFeature(
        key="grade_ordinal",
        label="Derived grade band",
        unit=None,
        guidance="Derived from average scores (A→5 … F→1).",
    ),
}


def human_label(feature_key: str) -> str:
    return HUMAN_FEATURES.get(feature_key, HumanFeature(feature_key, feature_key)).label


def human_unit(feature_key: str) -> str | None:
    return HUMAN_FEATURES.get(feature_key, HumanFeature(feature_key, feature_key)).unit
