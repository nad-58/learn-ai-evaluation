"""Utility functions for AI evaluation tutorials."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


@dataclass
class ClassificationMetrics:
    accuracy: float
    precision: float
    recall: float
    f1: float


def binary_classification_metrics(y_true, y_pred) -> ClassificationMetrics:
    """Calculate common metrics for binary classification."""
    return ClassificationMetrics(
        accuracy=float(accuracy_score(y_true, y_pred)),
        precision=float(precision_score(y_true, y_pred, zero_division=0)),
        recall=float(recall_score(y_true, y_pred, zero_division=0)),
        f1=float(f1_score(y_true, y_pred, zero_division=0)),
    )


def metrics_as_dict(metrics: ClassificationMetrics) -> Dict[str, float]:
    """Convert ClassificationMetrics to a dictionary."""
    return {
        "accuracy": metrics.accuracy,
        "precision": metrics.precision,
        "recall": metrics.recall,
        "f1": metrics.f1,
    }
