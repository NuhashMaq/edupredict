from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
import shap

from app.ml.model import EnsembleArtifact


@dataclass(frozen=True)
class FactorContribution:
    feature: str
    value: float
    impact: float
    direction: str  # "increases_risk" | "decreases_risk"


def explain_with_shap_tree(
    artifact: EnsembleArtifact,
    x_row: pd.DataFrame,
    *,
    top_k: int = 5,
) -> list[FactorContribution]:
    """SHAP-style explanation using the LightGBM component.

    Notes:
    - Uses TreeExplainer for speed.
    - Returns top-k absolute impacts.
    """

    x_row = x_row[artifact.feature_names]

    explainer = shap.TreeExplainer(artifact.lgbm)
    shap_values = explainer.shap_values(x_row)

    # Binary classification: shap may return list[class0, class1] or array.
    if isinstance(shap_values, list):
        sv = np.asarray(shap_values[1]).reshape(-1)
    else:
        sv = np.asarray(shap_values).reshape(-1)

    values = x_row.iloc[0].to_dict()

    pairs = []
    for idx, feat in enumerate(artifact.feature_names):
        impact = float(sv[idx])
        pairs.append(
            FactorContribution(
                feature=feat,
                value=float(values[feat]),
                impact=impact,
                direction="increases_risk" if impact >= 0 else "decreases_risk",
            )
        )

    pairs.sort(key=lambda p: abs(p.impact), reverse=True)
    return pairs[: max(1, top_k)]
