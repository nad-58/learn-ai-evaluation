"""Numerical example: class balance and feature distributions.

Run from the repository root:

    python examples/dataset-evaluation/class_balance_and_distributions_example.py
"""
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.dataset_quality import (
    categorical_cardinality_report,
    class_balance_report,
    feature_distribution_report,
)


def build_dataset() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "age": [22, 25, 31, 38, 41, 52, 63, 70, 29, 34],
            "score": [0.42, 0.55, 0.61, 0.67, 0.72, 0.78, 0.84, 0.91, 0.58, 0.64],
            "site": ["A", "A", "A", "B", "B", "B", "C", "C", "A", "B"],
            "label": [0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
        }
    )


def main() -> None:
    data = build_dataset()

    print("CLASS BALANCE")
    print(class_balance_report(data, target_column="label").to_string(index=False))

    print("\nNUMERIC FEATURE DISTRIBUTIONS")
    print(
        feature_distribution_report(
            data,
            numeric_columns=["age", "score"],
        ).round(4).to_string(index=False)
    )

    print("\nCATEGORICAL CARDINALITY")
    print(
        categorical_cardinality_report(
            data,
            categorical_columns=["site"],
        ).to_string(index=False)
    )

    print("\nINTERPRETATION")
    print("- class 0 has 7/10 rows = 70%")
    print("- class 1 has 3/10 rows = 30%")
    print("- site has three categories: A, B and C")


if __name__ == "__main__":
    main()
