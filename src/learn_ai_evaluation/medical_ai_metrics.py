"""Public-safe utilities for technical evaluation of medical AI models.

These functions support educational model evaluation only. They do not provide
clinical advice and do not determine whether a system is safe or suitable for
clinical use.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Iterable, Sequence


@dataclass(frozen=True)
class BinaryEvaluation:
    """Summary of binary classification performance."""

    true_positive: int
    true_negative: int
    false_positive: int
    false_negative: int
    sensitivity: float
    specificity: float
    precision: float
    negative_predictive_value: float
    accuracy: float
    balanced_accuracy: float


def _safe_divide(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def binary_evaluation(y_true: Sequence[int], y_pred: Sequence[int]) -> BinaryEvaluation:
    """Evaluate binary predictions labelled with 0 and 1.

    Raises:
        ValueError: If the inputs differ in length, are empty, or contain values
            other than 0 and 1.
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length")
    if not y_true:
        raise ValueError("at least one observation is required")
    if any(value not in (0, 1) for value in [*y_true, *y_pred]):
        raise ValueError("binary labels must be 0 or 1")

    tp = sum(t == 1 and p == 1 for t, p in zip(y_true, y_pred))
    tn = sum(t == 0 and p == 0 for t, p in zip(y_true, y_pred))
    fp = sum(t == 0 and p == 1 for t, p in zip(y_true, y_pred))
    fn = sum(t == 1 and p == 0 for t, p in zip(y_true, y_pred))

    sensitivity = _safe_divide(tp, tp + fn)
    specificity = _safe_divide(tn, tn + fp)
    precision = _safe_divide(tp, tp + fp)
    npv = _safe_divide(tn, tn + fn)
    accuracy = _safe_divide(tp + tn, len(y_true))
    balanced_accuracy = (sensitivity + specificity) / 2

    return BinaryEvaluation(
        true_positive=tp,
        true_negative=tn,
        false_positive=fp,
        false_negative=fn,
        sensitivity=sensitivity,
        specificity=specificity,
        precision=precision,
        negative_predictive_value=npv,
        accuracy=accuracy,
        balanced_accuracy=balanced_accuracy,
    )


def threshold_predictions(probabilities: Iterable[float], threshold: float = 0.5) -> list[int]:
    """Convert probabilities into binary predictions at a chosen threshold."""
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be between 0 and 1")

    predictions: list[int] = []
    for probability in probabilities:
        if not 0.0 <= probability <= 1.0:
            raise ValueError("probabilities must be between 0 and 1")
        predictions.append(int(probability >= threshold))
    return predictions


def wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    """Calculate a Wilson confidence interval for a binomial proportion."""
    if total <= 0:
        raise ValueError("total must be greater than zero")
    if successes < 0 or successes > total:
        raise ValueError("successes must be between zero and total")

    proportion = successes / total
    denominator = 1 + z * z / total
    centre = proportion + z * z / (2 * total)
    adjustment = z * sqrt(
        proportion * (1 - proportion) / total + z * z / (4 * total * total)
    )
    return (
        max(0.0, (centre - adjustment) / denominator),
        min(1.0, (centre + adjustment) / denominator),
    )


def site_level_evaluation(
    y_true: Sequence[int],
    y_pred: Sequence[int],
    site_ids: Sequence[str],
) -> dict[str, BinaryEvaluation]:
    """Calculate binary performance independently for each acquisition site."""
    if not (len(y_true) == len(y_pred) == len(site_ids)):
        raise ValueError("y_true, y_pred, and site_ids must have the same length")

    results: dict[str, BinaryEvaluation] = {}
    for site in sorted(set(site_ids)):
        indices = [index for index, value in enumerate(site_ids) if value == site]
        results[site] = binary_evaluation(
            [y_true[index] for index in indices],
            [y_pred[index] for index in indices],
        )
    return results


def dice_score(reference_mask: Sequence[int], predicted_mask: Sequence[int]) -> float:
    """Calculate Dice overlap for flattened binary masks."""
    if len(reference_mask) != len(predicted_mask):
        raise ValueError("masks must have the same number of elements")
    if any(value not in (0, 1) for value in [*reference_mask, *predicted_mask]):
        raise ValueError("mask values must be 0 or 1")

    intersection = sum(r == 1 and p == 1 for r, p in zip(reference_mask, predicted_mask))
    reference_size = sum(reference_mask)
    predicted_size = sum(predicted_mask)

    if reference_size + predicted_size == 0:
        return 1.0
    return 2 * intersection / (reference_size + predicted_size)
