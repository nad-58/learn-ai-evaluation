"""Numerical example: outlier screening and split leakage.

Run from the repository root:

    python examples/dataset-evaluation/outliers_and_leakage_example.py
"""
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.dataset_quality import outlier_report_iqr, split_leakage_report


def main() -> None:
    full_data = pd.DataFrame(
        {
            "sample_id": ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"],
            "age": [24, 27, 31, 35, 39, 42, 46, 120],
            "score": [0.51, 0.57, 0.61, 0.66, 0.70, 0.74, 0.79, 0.95],
        }
    )

    print("OUTLIER REPORT")
    print(
        outlier_report_iqr(
            full_data,
            numeric_columns=["age", "score"],
        ).round(4).to_string(index=False)
    )

    train = pd.DataFrame({"sample_id": ["s1", "s2", "s3", "s4", "s5"]})
    test = pd.DataFrame({"sample_id": ["s5", "s6", "s7"]})

    print("\nSPLIT LEAKAGE REPORT")
    print(split_leakage_report(train, test, columns=["sample_id"]))

    print("\nINTERPRETATION")
    print("- age 120 is screened as a potential outlier")
    print("- sample_id s5 occurs in both train and test")
    print("- test overlap is 1/3 = 33.33%, so the split must be corrected")


if __name__ == "__main__":
    main()
