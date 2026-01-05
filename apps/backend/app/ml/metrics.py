from __future__ import annotations

import numpy as np
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score


def evaluate_binary(y_true: np.ndarray, y_proba: np.ndarray) -> dict[str, float]:
    y_pred = (y_proba >= 0.5).astype(int)

    out: dict[str, float] = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
    }

    # ROC-AUC is undefined when only one class exists.
    try:
        out["roc_auc"] = float(roc_auc_score(y_true, y_proba))
    except Exception:
        out["roc_auc"] = float("nan")

    return out
