import pandas as pd

from learn_ai_evaluation.dataset_quality import (
    categorical_cardinality_report,
    class_balance_report,
    duplicate_report,
    feature_distribution_report,
    missing_value_report,
    outlier_report_iqr,
    render_markdown_report,
    split_leakage_report,
)


def build_dataset() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "sample_id": ["s1", "s2", "s3", "s3", "s4"],
            "age": [25, 41, None, 63, 120],
            "score": [0.72, 0.81, 0.66, 0.91, 0.99],
            "site": ["A", "A", "B", "B", None],
            "label": [0, 0, 0, 1, 1],
        }
    )


def test_missing_and_duplicate_reports():
    data = build_dataset()
    missing = missing_value_report(data)
    duplicates = duplicate_report(data, subset=["sample_id"])
    assert int(missing.loc[missing["column"] == "age", "missing_count"].iloc[0]) == 1
    assert duplicates["duplicate_rows"] == 2


def test_class_and_feature_reports():
    data = build_dataset()
    balance = class_balance_report(data, "label")
    numeric = feature_distribution_report(data, ["age", "score"])
    categorical = categorical_cardinality_report(data, ["site"])
    assert int(balance["count"].sum()) == len(data)
    assert set(numeric["column"]) == {"age", "score"}
    assert int(categorical.loc[0, "unique_values"]) == 2


def test_outlier_and_leakage_reports():
    data = build_dataset()
    outliers = outlier_report_iqr(data, ["age"])
    leakage = split_leakage_report(
        data.iloc[:3],
        data.iloc[2:],
        columns=["sample_id"],
    )
    assert "outlier_count" in outliers.columns
    assert leakage["overlapping_rows"] == 1


def test_markdown_report_contains_sections():
    report = render_markdown_report(build_dataset(), target_column="label")
    assert "# Dataset Quality Report" in report
    assert "## Missing values" in report
    assert "## Class balance" in report
