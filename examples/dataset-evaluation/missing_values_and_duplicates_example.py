"""Numerical example: missing values and duplicate records.

Run from the repository root:

    python examples/dataset-evaluation/missing_values_and_duplicates_example.py
"""
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.dataset_quality import duplicate_report, missing_value_report


def build_dataset() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "sample_id": ["s1", "s2", "s3", "s3", "s4", "s5"],
            "age": [25, 41, None, None, 63, 52],
            "score": [0.72, 0.81, 0.66, 0.66, None, 0.73],
            "label": [0, 0, 1, 1, 1, 0],
        }
    )


def main() -> None:
    data = build_dataset()
    print("DATASET")
    print(data.to_string(index=False))

    print("\nMISSING-VALUE REPORT")
    print(missing_value_report(data).to_string(index=False))

    print("\nDUPLICATE-ID REPORT")
    print(duplicate_report(data, subset=["sample_id"]))

    print("\nINTERPRETATION")
    print("- age has 2 missing values out of 6 rows = 33.33%")
    print("- score has 1 missing value out of 6 rows = 16.67%")
    print("- sample_id s3 appears twice, so 2 rows are marked as duplicates")


if __name__ == "__main__":
    main()
