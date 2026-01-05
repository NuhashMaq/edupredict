from __future__ import annotations

import argparse

import pandas as pd

from app.ml.dataset import DatasetConfig
from app.ml.train import TrainConfig, train_from_dataframe


def main() -> int:
    parser = argparse.ArgumentParser(description="Train EduPredict models and write versioned artifacts.")
    parser.add_argument("--csv", required=True, help="Path to CSV with academic record columns.")
    parser.add_argument("--label-column", default="at_risk", help="Optional label column name.")
    parser.add_argument("--notes", default="", help="Optional notes stored in metadata.")

    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    version, meta = train_from_dataframe(
        df,
        dataset_cfg=DatasetConfig(label_column=args.label_column),
        train_cfg=TrainConfig(),
        notes=args.notes,
    )

    print(f"Trained and saved model version: {version}")
    print(f"Metrics: {meta.metrics}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
