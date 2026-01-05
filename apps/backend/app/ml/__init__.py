"""ML package for EduPredict.

Design goals:
- Reproducible training and artifact versioning
- Stable inference contract (features, outputs)
- Explainability primitives (SHAP-style contributions)

The training pipeline intentionally separates:
- dataset parsing/validation
- preprocessing
- model training
- registry I/O
"""
