from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from app.ml.features import FEATURES, feature_names


@dataclass(frozen=True)
class PreprocessConfig:
    pct_clip_low: int = 0
    pct_clip_high: int = 100
    gpa_clip_low: float = 0.0
    gpa_clip_high: float = 4.0


def grade_ordinal_from_percent(avg_pct: pd.Series) -> pd.Series:
    """Encode letter-grade buckets into an ordinal scale.

    This is intentionally monotonic and interpretable.

    Mapping:
    A(>=90)->5, B(>=80)->4, C(>=70)->3, D(>=60)->2, F(<60)->1
    """

    bins = [-np.inf, 60, 70, 80, 90, np.inf]
    labels = [1, 2, 3, 4, 5]
    return pd.cut(avg_pct, bins=bins, labels=labels).astype("int64")


def preprocess_records(df: pd.DataFrame, *, cfg: PreprocessConfig | None = None) -> pd.DataFrame:
    """Preprocess raw academic records into model-ready features.

    - Handles missing values via median imputation
    - Clips outliers to domain ranges (percentages 0-100; GPA 0-4)
    - Adds grade_ordinal derived from average percentage

    Returns a new dataframe containing only the canonical feature columns.
    """

    cfg = cfg or PreprocessConfig()

    required = [
        "attendance_pct",
        "assignments_pct",
        "quizzes_pct",
        "exams_pct",
        "gpa",
    ]
    missing_cols = [c for c in required if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    x = df.copy()

    # Coerce numeric
    for col in ["attendance_pct", "assignments_pct", "quizzes_pct", "exams_pct"]:
        x[col] = pd.to_numeric(x[col], errors="coerce")
        x[col] = x[col].clip(cfg.pct_clip_low, cfg.pct_clip_high)

    x["gpa"] = pd.to_numeric(x["gpa"], errors="coerce")
    x["gpa"] = x["gpa"].clip(cfg.gpa_clip_low, cfg.gpa_clip_high)

    # Median imputation
    for col in required:
        med = float(np.nanmedian(x[col].to_numpy(dtype=float)))
        x[col] = x[col].fillna(med)

    avg_pct = (x["assignments_pct"] + x["quizzes_pct"] + x["exams_pct"]) / 3.0
    x[FEATURES.grade_ordinal] = grade_ordinal_from_percent(avg_pct)

    return x[feature_names()].astype("float64")
