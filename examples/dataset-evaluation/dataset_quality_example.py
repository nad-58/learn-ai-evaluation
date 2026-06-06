"""Runnable example for dataset quality evaluation.

Run from the repository root:

    python examples/dataset-evaluation/dataset_quality_example.py

This example uses a small synthetic dataset so it can be shared publicly and run
without external data.
"""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.dataset_quality import (  # noqa: E402
    categorical_cardinality_report,
    class_balance_report,
    duplicate_report,
    feature_distribution_report,
    missing_value_report,
    outlier_report_iqr,
    render_markdown_report,
    split_leakage_report,
)


def build_synthetic_dataset() -> pd.DataFrame:
    """Create a small dataset with common quality issues."""
    return pd.DataFrame(
        {
            "sample_id": ["s1", "s2", "s3", "s4", "s5", "s5", "s6", "s7", "s8", "s9"],
            "age": [25, 41, 39, None, 63, 63, 29, 31, 120, 52],
            "score": [0.72, 0.81, None, 0.66, 0.91, 0.91, 0.40, 0.44, 0.99, 0.73],
            "site": ["A", "A", "B", "B", "C", "C", "A", None, "B", "C"],
            "label": [0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
        }
    )


def main() -> None:
    df = build_synthetic_dataset()

    print("\nMissing values")
    print(missing_value_report(df))

    print("\nDuplicates based on sample_id")
    print(duplicate_report(df, subset=["sample_id"]))

    print("\nClass balance")
    print(class_balance_report(df, target_column="label"))

    print("\nNumeric feature distribution")
    print(feature_distribution_report(df, numeric_columns=["age", "score"]))

    print("\nCategorical feature cardinality")
    print(categorical_cardinality_report(df, categorical_columns=["site"]))

    print("\nPotential outliers")
    print(outlier_report_iqr(df, numeric_columns=["age", "score"]))

    train_df, test_df = train_test_split(
        df,
        test_size=0.3,
        random_state=7,
        stratify=df["label"],
    )

    print("\nExact split leakage check")
    print(split_leakage_report(train_df, test_df, columns=["sample_id"]))

    print("\nMarkdown report preview")
    print(render_markdown_report(df, target_column="label"))


if __name__ == "__main__":
    main()
