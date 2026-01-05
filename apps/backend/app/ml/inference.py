from __future__ import annotations

import uuid
from dataclasses import dataclass
from functools import lru_cache

import pandas as pd
from fastapi import HTTPException, status

from app.ml.explain import FactorContribution, explain_with_shap_tree
from app.ml.preprocess import preprocess_records
from app.ml.registry import latest_version, load_latest_artifact, load_metadata
from app.models.academic_record import AcademicRecord


@dataclass(frozen=True)
class LoadedModel:
    version: str
    artifact: object
    metadata: object


def _service_unavailable(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)


@lru_cache
def get_loaded_model() -> LoadedModel:
    v = latest_version()
    if not v:
        raise _service_unavailable("No model is available yet. Train and register a model first.")

    try:
        artifact = load_latest_artifact()
        meta = load_metadata(v)
    except FileNotFoundError:
        raise _service_unavailable("Model registry is missing artifacts. Retrain the model.")

    return LoadedModel(version=v, artifact=artifact, metadata=meta)


def clear_model_cache() -> None:
    # Test / ops utility
    get_loaded_model.cache_clear()


def df_from_record(record: AcademicRecord) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "attendance_pct": record.attendance_pct,
                "assignments_pct": record.assignments_pct,
                "quizzes_pct": record.quizzes_pct,
                "exams_pct": record.exams_pct,
                "gpa": record.gpa,
            }
        ]
    )


def df_from_features(*, attendance_pct: int, assignments_pct: int, quizzes_pct: int, exams_pct: int, gpa: float) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "attendance_pct": attendance_pct,
                "assignments_pct": assignments_pct,
                "quizzes_pct": quizzes_pct,
                "exams_pct": exams_pct,
                "gpa": gpa,
            }
        ]
    )


def predict_proba_from_raw_df(df_raw: pd.DataFrame) -> tuple[float, str]:
    loaded = get_loaded_model()
    x = preprocess_records(df_raw)
    p = float(loaded.artifact.predict_proba(x)[0])
    return p, loaded.version


def explain_from_raw_df(df_raw: pd.DataFrame, *, top_k: int = 5) -> tuple[list[FactorContribution], str]:
    loaded = get_loaded_model()
    x = preprocess_records(df_raw)
    factors = explain_with_shap_tree(loaded.artifact, x.iloc[[0]], top_k=top_k)
    return factors, loaded.version
