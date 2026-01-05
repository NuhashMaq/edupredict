from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from app.ml.registry import latest_version, load_latest_artifact
from app.ml.train import train_from_dataframe


def test_train_saves_and_loads_artifact(tmp_path, monkeypatch):
    # Redirect registry to a temp directory.
    monkeypatch.setenv("MODEL_REGISTRY_PATH", str(tmp_path / "registry"))

    rng = np.random.default_rng(42)
    n = 250

    df = pd.DataFrame(
        {
            "attendance_pct": rng.integers(50, 100, size=n),
            "assignments_pct": rng.integers(40, 100, size=n),
            "quizzes_pct": rng.integers(35, 100, size=n),
            "exams_pct": rng.integers(30, 100, size=n),
            "gpa": rng.random(size=n) * 4.0,
        }
    )

    # Provide an explicit label for determinism.
    avg = (df["assignments_pct"] + df["quizzes_pct"] + df["exams_pct"]) / 3.0
    df["at_risk"] = ((df["gpa"] < 2.2) | (df["attendance_pct"] < 78) | (avg < 66)).astype(int)

    version, meta = train_from_dataframe(df, notes="test")
    assert version
    assert meta.metrics

    v2 = latest_version()
    assert v2 == version

    artifact = load_latest_artifact()

    # Basic inference contract
    x1 = df.iloc[:1].drop(columns=["at_risk"])
    # train_from_dataframe expects raw df, artifact expects preprocessed feature columns.
    # We use the pipeline's internal preprocess in training, so we just validate artifact executes
    # on preprocessed inputs here via a minimal reconstruction.
    from app.ml.preprocess import preprocess_records

    x_proc = preprocess_records(x1)
    p = artifact.predict_proba(x_proc)
    assert p.shape == (1,)
    assert float(p[0]) >= 0.0 and float(p[0]) <= 1.0
