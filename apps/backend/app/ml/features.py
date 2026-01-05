from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureSpec:
    """Canonical model feature contract.

    These are the only features the model expects at inference time.
    """

    attendance_pct: str = "attendance_pct"
    assignments_pct: str = "assignments_pct"
    quizzes_pct: str = "quizzes_pct"
    exams_pct: str = "exams_pct"
    gpa: str = "gpa"
    grade_ordinal: str = "grade_ordinal"


FEATURES = FeatureSpec()


def feature_names() -> list[str]:
    return [
        FEATURES.attendance_pct,
        FEATURES.assignments_pct,
        FEATURES.quizzes_pct,
        FEATURES.exams_pct,
        FEATURES.gpa,
        FEATURES.grade_ordinal,
    ]
