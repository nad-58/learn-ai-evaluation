"""Dataset quality utilities for Learn AI Evaluation.

These helpers support public-safe dataset evaluation examples. They are intended
for educational use before model training and before reporting model metrics.
"""

from __future__ import annotations

from typing import Optional, Sequence
import hashlib

import numpy as np
import pandas as pd


def _safe_percent(count: float, total: float) -> float:
    """Return percentage safely when total may be zero."""
    if total == 0:
        return 0.0
    return float((count / total) * 100.0)


def missing_value_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return missing-value count and percentage for every column."""
    total_rows = len(df)
    report = pd.DataFrame(
        {
            "column": df.columns,
            "missing_count": [int(df[col].isna().sum()) for col in df.columns],
            "missing_percent": [
                _safe_percent(float(df[col].isna().sum()), float(total_rows))
                for col in df.columns
            ],
            "dtype": [str(df[col].dtype) for col in df.columns],
        }
    )
    return report.sort_values(
        ["missing_percent", "missing_count"], ascending=False
    ).reset_index(drop=True)


def duplicate_report(df: pd.DataFrame, subset: Optional[Sequence[str]] = None) -> dict:
    """Return duplicate row statistics.

    Use subset when duplication should be checked using identifiers, filenames,
    subject IDs, or other entity-level keys.
    """
    duplicate_mask = df.duplicated(subset=subset, keep=False)
    duplicate_rows = int(duplicate_mask.sum())
    return {
        "total_rows": int(len(df)),
        "duplicate_rows": duplicate_rows,
        "duplicate_percent": _safe_percent(float(duplicate_rows), float(len(df))),
        "subset": list(subset) if subset is not None else "all_columns",
    }


def class_balance_report(df: pd.DataFrame, target_column: str) -> pd.DataFrame:
    """Return class counts and percentages for a target label column."""
    if target_column not in df.columns:
        raise ValueError(f"target_column '{target_column}' was not found")

    counts = df[target_column].value_counts(dropna=False)
    percentages = df[target_column].value_counts(normalize=True, dropna=False) * 100.0
    return pd.DataFrame(
        {
            "class_label": counts.index.astype(str),
            "count": counts.values,
            "percent": percentages.values,
        }
    ).sort_values("count", ascending=False).reset_index(drop=True)


def feature_distribution_report(
    df: pd.DataFrame, numeric_columns: Optional[Sequence[str]] = None
) -> pd.DataFrame:
    """Return descriptive statistics for numeric features."""
    if numeric_columns is None:
        numeric_columns = list(df.select_dtypes(include=[np.number]).columns)

    rows = []
    for col in numeric_columns:
        if col not in df.columns:
            continue
        series = pd.to_numeric(df[col], errors="coerce")
        rows.append(
            {
                "column": col,
                "count": int(series.notna().sum()),
                "mean": float(series.mean()) if series.notna().any() else np.nan,
                "std": float(series.std()) if series.notna().sum() > 1 else np.nan,
                "min": float(series.min()) if series.notna().any() else np.nan,
                "p25": float(series.quantile(0.25)) if series.notna().any() else np.nan,
                "median": float(series.median()) if series.notna().any() else np.nan,
                "p75": float(series.quantile(0.75)) if series.notna().any() else np.nan,
                "max": float(series.max()) if series.notna().any() else np.nan,
            }
        )
    return pd.DataFrame(rows)


def categorical_cardinality_report(
    df: pd.DataFrame, categorical_columns: Optional[Sequence[str]] = None
) -> pd.DataFrame:
    """Return cardinality and missingness for categorical features."""
    if categorical_columns is None:
        categorical_columns = list(
            df.select_dtypes(include=["object", "category", "bool"]).columns
        )

    rows = []
    for col in categorical_columns:
        if col not in df.columns:
            continue
        non_missing = df[col].dropna()
        rows.append(
            {
                "column": col,
                "unique_values": int(df[col].nunique(dropna=True)),
                "missing_count": int(df[col].isna().sum()),
                "missing_percent": _safe_percent(float(df[col].isna().sum()), float(len(df))),
                "most_common_value": None if non_missing.empty else str(non_missing.mode().iloc[0]),
            }
        )
    return pd.DataFrame(rows).sort_values("unique_values", ascending=False).reset_index(drop=True)


def outlier_report_iqr(
    df: pd.DataFrame,
    numeric_columns: Optional[Sequence[str]] = None,
    multiplier: float = 1.5,
) -> pd.DataFrame:
    """Screen numeric columns for potential outliers using the IQR rule."""
    if numeric_columns is None:
        numeric_columns = list(df.select_dtypes(include=[np.number]).columns)

    rows = []
    for col in numeric_columns:
        if col not in df.columns:
            continue
        series = pd.to_numeric(df[col], errors="coerce").dropna()
        if series.empty:
            rows.append(
                {"column": col, "outlier_count": 0, "outlier_percent": 0.0}
            )
            continue
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - multiplier * iqr
        upper = q3 + multiplier * iqr
        outlier_count = int(((series < lower) | (series > upper)).sum())
        rows.append(
            {
                "column": col,
                "outlier_count": outlier_count,
                "outlier_percent": _safe_percent(float(outlier_count), float(len(series))),
                "lower_bound": float(lower),
                "upper_bound": float(upper),
            }
        )
    return pd.DataFrame(rows).sort_values("outlier_percent", ascending=False).reset_index(drop=True)


def row_hashes(df: pd.DataFrame, columns: Optional[Sequence[str]] = None) -> pd.Series:
    """Create stable row hashes for exact overlap checks."""
    if columns is None:
        columns = list(df.columns)
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"Columns not found: {missing}")

    def hash_row(row: pd.Series) -> str:
        text = "||".join("<NA>" if pd.isna(value) else str(value) for value in row.values)
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    return df[list(columns)].apply(hash_row, axis=1)


def split_leakage_report(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    columns: Optional[Sequence[str]] = None,
) -> dict:
    """Check exact row overlap between train and test data."""
    train_hashes = set(row_hashes(train_df, columns=columns))
    test_hashes = set(row_hashes(test_df, columns=columns))
    overlap = train_hashes.intersection(test_hashes)
    return {
        "train_rows": int(len(train_df)),
        "test_rows": int(len(test_df)),
        "overlapping_rows": int(len(overlap)),
        "overlap_percent_of_test": _safe_percent(float(len(overlap)), float(len(test_df))),
        "columns_used": list(columns) if columns is not None else "all_columns",
    }


def render_markdown_report(df: pd.DataFrame, target_column: Optional[str] = None) -> str:
    """Render a compact dataset quality report in Markdown."""
    sections = ["# Dataset Quality Report", "", "## Shape", ""]
    sections.append(f"- Rows: {df.shape[0]}")
    sections.append(f"- Columns: {df.shape[1]}")
    sections.extend(["", "## Missing values", "", missing_value_report(df).to_markdown(index=False)])
    sections.extend(["", "## Duplicates", ""])
    for key, value in duplicate_report(df).items():
        sections.append(f"- {key}: {value}")
    if target_column is not None:
        sections.extend(["", "## Class balance", "", class_balance_report(df, target_column).to_markdown(index=False)])
    numeric = feature_distribution_report(df)
    if not numeric.empty:
        sections.extend(["", "## Numeric feature distribution", "", numeric.to_markdown(index=False)])
    outliers = outlier_report_iqr(df)
    if not outliers.empty:
        sections.extend(["", "## Potential outliers", "", outliers.to_markdown(index=False)])
    categorical = categorical_cardinality_report(df)
    if not categorical.empty:
        sections.extend(["", "## Categorical feature cardinality", "", categorical.to_markdown(index=False)])
    return "\n".join(sections)
