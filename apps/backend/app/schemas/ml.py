from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class PredictFromFeatures(BaseModel):
    attendance_pct: int = Field(ge=0, le=100)
    assignments_pct: int = Field(ge=0, le=100)
    quizzes_pct: int = Field(ge=0, le=100)
    exams_pct: int = Field(ge=0, le=100)
    gpa: float = Field(ge=0.0, le=4.0)


class PredictionRequest(BaseModel):
    # Provide ONE of: academic_record_id, student_user_id, or features.
    academic_record_id: uuid.UUID | None = None
    student_user_id: uuid.UUID | None = None
    features: PredictFromFeatures | None = None

    threshold: float = Field(default=0.5, ge=0.0, le=1.0)


class PredictionResponse(BaseModel):
    classification: str  # "At-Risk" | "Not-At-Risk"
    risk_probability: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    threshold: float = Field(ge=0.0, le=1.0)
    model_version: str


class ExplainRequest(BaseModel):
    academic_record_id: uuid.UUID | None = None
    student_user_id: uuid.UUID | None = None
    features: PredictFromFeatures | None = None

    top_k: int = Field(default=5, ge=1, le=10)


class FactorPublic(BaseModel):
    feature_key: str
    feature_label: str
    value: float
    impact: float
    direction: str
    unit: str | None = None


class ExplainResponse(BaseModel):
    model_version: str
    factors: list[FactorPublic]


class ModelInfo(BaseModel):
    model_version: str
    created_at: datetime | str
    metrics: dict[str, float]
    feature_names: list[str]
    notes: str = ""


class TrainRequest(BaseModel):
    notes: str = Field(default="", max_length=500)
    min_rows: int = Field(default=20, ge=5, le=10000)


class TrainResponse(BaseModel):
    trained: bool = True
    model: ModelInfo


class ModelListResponse(BaseModel):
    latest_version: str | None = None
    items: list[ModelInfo]


class PromoteResponse(BaseModel):
    latest_version: str
    model: ModelInfo
