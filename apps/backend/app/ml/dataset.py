from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from app.ml.preprocess import preprocess_records


@dataclass(frozen=True)
class DatasetConfig:
    """Controls labeling and parsing.

    For production, provide an explicit label column (recommended).
    If absent, a conservative heuristic label is derived to enable demos.
    """

    label_column: str = "at_risk"


def derive_at_risk_label(df: pd.DataFrame) -> pd.Series:
    """Heuristic label for demos when ground-truth isn't available.

    A student is labeled At-Risk if any of the following holds:
    - GPA < 2.0
    - Attendance < 75%
    - Average score < 65%

    This is a placeholder to make the pipeline runnable end-to-end.
    In production, replace with a dataset that includes outcome labels.
    """

    # NOTE: Some demo datasets (including our seeded SQLite DB) may contain a score column
    # that is effectively missing (e.g., `quizzes_pct` is 0 for all rows). Including that
    # in the average can collapse labels to a single class and make training impossible.
    score_parts: list[pd.Series] = []
    for col in ("assignments_pct", "quizzes_pct", "exams_pct"):
        if col not in df.columns:
            continue
        s = pd.to_numeric(df[col], errors="coerce")
        # Treat a score column as missing if it's all NaN or all zeros.
        if not s.notna().any():
            continue
        if (s.fillna(0) == 0).all():
            continue
        score_parts.append(s)

    if score_parts:
        avg_pct = sum(score_parts) / float(len(score_parts))
    else:
        # No usable score columns; fall back to the other signals.
        avg_pct = pd.Series(np.nan, index=df.index)

    gpa = pd.to_numeric(df.get("gpa"), errors="coerce")
    attendance = pd.to_numeric(df.get("attendance_pct"), errors="coerce")

    risk = (gpa < 2.0) | (attendance < 75) | (avg_pct < 65)
    return risk.fillna(False).astype(int)


def build_training_matrices(df_raw: pd.DataFrame, *, cfg: DatasetConfig | None = None) -> tuple[pd.DataFrame, np.ndarray]:
    cfg = cfg or DatasetConfig()

    x = preprocess_records(df_raw)

    if cfg.label_column in df_raw.columns:
        y = pd.to_numeric(df_raw[cfg.label_column], errors="coerce").fillna(0).astype(int).to_numpy()
    else:
        y = derive_at_risk_label(df_raw).to_numpy()

    y = np.clip(y, 0, 1).astype(int)
    return x, y
