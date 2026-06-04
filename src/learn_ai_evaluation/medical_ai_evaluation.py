"""Medical AI evaluation utilities for Learn AI Evaluation.

This module is educational and public-safe. It focuses on technical model and
system evaluation for medical AI examples, not clinical validation, regulatory
approval, or claims of clinical safety/effectiveness.

The functions use small NumPy-based examples so learners can understand metric
logic before adapting the ideas to more formal evaluation pipelines.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Sequence

import numpy as np


ArrayLike = Sequence[float] | np.ndarray


def _as_numpy(values: ArrayLike) -> np.ndarray:
    """Convert values to a NumPy array."""
    return np.asarray(values)


def safe_divide(numerator: float, denominator: float) -> float:
    """Return numerator / denominator, or 0.0 when denominator is zero."""
    if denominator == 0:
        return 0.0
    return float(numerator / denominator)


def binary_confusion_counts(
    y_true: Sequence[int],
    y_score: Sequence[float],
    threshold: float = 0.5,
) -> dict[str, int]:
    """Return TP, FP, TN, and FN for a binary medical AI classifier.

    Parameters
    ----------
    y_true:
        Ground-truth labels where 1 means the target condition is present and
        0 means it is absent.
    y_score:
        Model scores or probabilities for the positive class.
    threshold:
        Decision threshold used to convert scores into binary predictions.
    """
    true = _as_numpy(y_true).astype(int)
    score = _as_numpy(y_score).astype(float)
    if true.shape[0] != score.shape[0]:
        raise ValueError("y_true and y_score must contain the same number of items")

    pred = (score >= threshold).astype(int)
    tp = int(np.sum((true == 1) & (pred == 1)))
    fp = int(np.sum((true == 0) & (pred == 1)))
    tn = int(np.sum((true == 0) & (pred == 0)))
    fn = int(np.sum((true == 1) & (pred == 0)))
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn}


def diagnostic_metric_summary(counts: dict[str, int]) -> dict[str, float]:
    """Return common diagnostic-style metrics from binary confusion counts."""
    tp = counts.get("tp", 0)
    fp = counts.get("fp", 0)
    tn = counts.get("tn", 0)
    fn = counts.get("fn", 0)

    sensitivity = safe_divide(tp, tp + fn)
    specificity = safe_divide(tn, tn + fp)
    precision = safe_divide(tp, tp + fp)
    negative_predictive_value = safe_divide(tn, tn + fn)
    accuracy = safe_divide(tp + tn, tp + tn + fp + fn)
    f1 = safe_divide(2 * precision * sensitivity, precision + sensitivity)
    balanced_accuracy = (sensitivity + specificity) / 2
    false_positive_rate = safe_divide(fp, fp + tn)
    false_negative_rate = safe_divide(fn, fn + tp)

    return {
        "sensitivity_recall": sensitivity,
        "specificity": specificity,
        "precision_ppv": precision,
        "negative_predictive_value": negative_predictive_value,
        "accuracy": accuracy,
        "balanced_accuracy": balanced_accuracy,
        "f1": f1,
        "false_positive_rate": false_positive_rate,
        "false_negative_rate": false_negative_rate,
    }


def threshold_sweep(
    y_true: Sequence[int],
    y_score: Sequence[float],
    thresholds: Optional[Iterable[float]] = None,
) -> list[dict[str, float | int]]:
    """Evaluate binary classification metrics over multiple thresholds."""
    if thresholds is None:
        thresholds = np.linspace(0.0, 1.0, 21)

    rows: list[dict[str, float | int]] = []
    for threshold in thresholds:
        counts = binary_confusion_counts(y_true, y_score, float(threshold))
        metrics = diagnostic_metric_summary(counts)
        rows.append({"threshold": float(threshold), **counts, **metrics})
    return rows


def select_threshold_for_minimum_sensitivity(
    y_true: Sequence[int],
    y_score: Sequence[float],
    minimum_sensitivity: float,
    thresholds: Optional[Iterable[float]] = None,
) -> dict[str, float | int]:
    """Select the highest-specificity threshold that meets minimum sensitivity.

    This is a technical example only. Real projects should define threshold
    criteria before testing and document the rationale carefully.
    """
    candidates = threshold_sweep(y_true, y_score, thresholds)
    passing = [row for row in candidates if row["sensitivity_recall"] >= minimum_sensitivity]
    if not passing:
        raise ValueError("No threshold met the minimum sensitivity requirement")
    return max(passing, key=lambda row: (row["specificity"], row["threshold"]))


def calibration_bins(
    y_true: Sequence[int],
    y_score: Sequence[float],
    n_bins: int = 10,
) -> list[dict[str, float | int]]:
    """Return simple calibration-bin statistics for binary probabilities."""
    if n_bins <= 0:
        raise ValueError("n_bins must be a positive integer")

    true = _as_numpy(y_true).astype(int)
    score = np.clip(_as_numpy(y_score).astype(float), 0.0, 1.0)
    if true.shape[0] != score.shape[0]:
        raise ValueError("y_true and y_score must contain the same number of items")

    bins = np.linspace(0.0, 1.0, n_bins + 1)
    rows: list[dict[str, float | int]] = []
    for index in range(n_bins):
        lower = bins[index]
        upper = bins[index + 1]
        if index == n_bins - 1:
            mask = (score >= lower) & (score <= upper)
        else:
            mask = (score >= lower) & (score < upper)
        count = int(np.sum(mask))
        rows.append({
            "bin_lower": float(lower),
            "bin_upper": float(upper),
            "count": count,
            "mean_score": float(np.mean(score[mask])) if count else 0.0,
            "observed_event_rate": float(np.mean(true[mask])) if count else 0.0,
            "absolute_gap": abs(
                (float(np.mean(score[mask])) if count else 0.0)
                - (float(np.mean(true[mask])) if count else 0.0)
            ),
        })
    return rows


def expected_calibration_error(
    y_true: Sequence[int],
    y_score: Sequence[float],
    n_bins: int = 10,
) -> float:
    """Return a simple expected calibration error for binary probabilities."""
    rows = calibration_bins(y_true, y_score, n_bins)
    total = sum(int(row["count"]) for row in rows)
    if total == 0:
        return 0.0
    return float(sum((int(row["count"]) / total) * float(row["absolute_gap"]) for row in rows))


@dataclass(frozen=True)
class GroupPerformance:
    """Compact summary of performance for one subgroup."""

    group: str
    count: int
    sensitivity_recall: float
    specificity: float
    precision_ppv: float
    balanced_accuracy: float


def subgroup_diagnostic_summary(
    y_true: Sequence[int],
    y_score: Sequence[float],
    groups: Sequence[str],
    threshold: float = 0.5,
    minimum_group_size: int = 1,
) -> list[GroupPerformance]:
    """Return diagnostic-style metrics for each subgroup.

    Groups can represent general categories such as site, scanner type, image
    quality band, acquisition protocol, or demographic grouping. Keep subgroup
    definitions appropriate, justified, and privacy-preserving.
    """
    true = _as_numpy(y_true).astype(int)
    score = _as_numpy(y_score).astype(float)
    group_array = _as_numpy(groups).astype(str)
    if not (true.shape[0] == score.shape[0] == group_array.shape[0]):
        raise ValueError("y_true, y_score, and groups must contain the same number of items")

    summaries: list[GroupPerformance] = []
    for group in sorted(set(group_array.tolist())):
        mask = group_array == group
        if int(np.sum(mask)) < minimum_group_size:
            continue
        counts = binary_confusion_counts(true[mask], score[mask], threshold)
        metrics = diagnostic_metric_summary(counts)
        summaries.append(GroupPerformance(
            group=str(group),
            count=int(np.sum(mask)),
            sensitivity_recall=float(metrics["sensitivity_recall"]),
            specificity=float(metrics["specificity"]),
            precision_ppv=float(metrics["precision_ppv"]),
            balanced_accuracy=float(metrics["balanced_accuracy"]),
        ))
    return summaries


def segmentation_volume_difference(
    mask_true: np.ndarray,
    mask_pred: np.ndarray,
    voxel_volume: float = 1.0,
) -> dict[str, float]:
    """Compare positive segmentation volume between reference and prediction."""
    true = _as_numpy(mask_true).astype(bool)
    pred = _as_numpy(mask_pred).astype(bool)
    if true.shape != pred.shape:
        raise ValueError("mask_true and mask_pred must have the same shape")
    if voxel_volume <= 0:
        raise ValueError("voxel_volume must be positive")

    true_volume = float(np.sum(true) * voxel_volume)
    pred_volume = float(np.sum(pred) * voxel_volume)
    absolute_difference = abs(pred_volume - true_volume)
    relative_difference = safe_divide(absolute_difference, true_volume)
    return {
        "reference_volume": true_volume,
        "predicted_volume": pred_volume,
        "absolute_volume_difference": absolute_difference,
        "relative_volume_difference": relative_difference,
    }
