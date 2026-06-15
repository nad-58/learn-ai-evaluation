"""Transparent group-fairness metrics for binary classification.

The functions are educational and domain-neutral. Fairness is contextual: no single
metric is universally appropriate, and different criteria can conflict.
"""
from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix


def _as_1d(values: Iterable[object], name: str) -> np.ndarray:
    array = np.asarray(list(values))
    if array.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if len(array) == 0:
        raise ValueError(f"{name} must not be empty")
    return array


def group_confusion_rates(
    y_true: Iterable[int],
    y_pred: Iterable[int],
    groups: Iterable[object],
    *,
    group_name: str = "group",
) -> pd.DataFrame:
    """Return outcome and error rates for each group."""
    truth = _as_1d(y_true, "y_true").astype(int)
    prediction = _as_1d(y_pred, "y_pred").astype(int)
    group_values = _as_1d(groups, "groups")
    if not (len(truth) == len(prediction) == len(group_values)):
        raise ValueError("y_true, y_pred, and groups must have the same length")
    if np.any(~np.isin(truth, [0, 1])) or np.any(~np.isin(prediction, [0, 1])):
        raise ValueError("y_true and y_pred must contain only binary values")

    rows: list[dict[str, object]] = []
    for group in pd.unique(group_values):
        mask = group_values == group
        tn, fp, fn, tp = confusion_matrix(
            truth[mask], prediction[mask], labels=[0, 1]
        ).ravel()
        n = int(mask.sum())
        actual_positive = tp + fn
        actual_negative = tn + fp
        predicted_positive = tp + fp
        rows.append(
            {
                group_name: group,
                "n": n,
                "actual_positive_rate": actual_positive / n if n else np.nan,
                "selection_rate": predicted_positive / n if n else np.nan,
                "true_positive_rate": tp / actual_positive if actual_positive else np.nan,
                "false_positive_rate": fp / actual_negative if actual_negative else np.nan,
                "positive_predictive_value": tp / predicted_positive if predicted_positive else np.nan,
                "true_negative_rate": tn / actual_negative if actual_negative else np.nan,
                "false_negative_rate": fn / actual_positive if actual_positive else np.nan,
                "tp": int(tp),
                "fp": int(fp),
                "fn": int(fn),
                "tn": int(tn),
            }
        )
    return pd.DataFrame(rows).sort_values(group_name).reset_index(drop=True)


def fairness_gap_summary(
    group_rates: pd.DataFrame,
    metrics: tuple[str, ...] = (
        "selection_rate",
        "true_positive_rate",
        "false_positive_rate",
        "positive_predictive_value",
    ),
) -> pd.DataFrame:
    """Summarise absolute gaps and worst-to-best ratios across groups."""
    rows = []
    for metric in metrics:
        if metric not in group_rates.columns:
            raise KeyError(f"metric {metric!r} was not found")
        values = group_rates[metric].dropna().astype(float)
        if values.empty:
            rows.append(
                {
                    "metric": metric,
                    "best": np.nan,
                    "worst": np.nan,
                    "absolute_gap": np.nan,
                    "worst_to_best_ratio": np.nan,
                }
            )
            continue
        best = float(values.max())
        worst = float(values.min())
        rows.append(
            {
                "metric": metric,
                "best": best,
                "worst": worst,
                "absolute_gap": best - worst,
                "worst_to_best_ratio": worst / best if best else np.nan,
            }
        )
    return pd.DataFrame(rows)


def demographic_parity_ratio(
    group_rates: pd.DataFrame,
    reference_group: object,
    comparison_group: object,
    *,
    group_column: str = "group",
) -> float:
    """Return comparison selection rate divided by reference selection rate."""
    reference = group_rates.loc[
        group_rates[group_column] == reference_group, "selection_rate"
    ]
    comparison = group_rates.loc[
        group_rates[group_column] == comparison_group, "selection_rate"
    ]
    if len(reference) != 1 or len(comparison) != 1:
        raise ValueError("reference and comparison groups must each identify one row")
    reference_rate = float(reference.iloc[0])
    return float(comparison.iloc[0] / reference_rate) if reference_rate else np.nan


def equalized_odds_gaps(group_rates: pd.DataFrame) -> dict[str, float]:
    """Return maximum between-group TPR and FPR gaps."""
    tpr = group_rates["true_positive_rate"].dropna().astype(float)
    fpr = group_rates["false_positive_rate"].dropna().astype(float)
    return {
        "true_positive_rate_gap": float(tpr.max() - tpr.min()) if not tpr.empty else np.nan,
        "false_positive_rate_gap": float(fpr.max() - fpr.min()) if not fpr.empty else np.nan,
    }
