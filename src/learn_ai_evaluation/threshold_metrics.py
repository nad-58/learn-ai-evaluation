"""Utilities for threshold-based binary classifier evaluation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ThresholdResult:
    threshold: float
    tp: int
    fp: int
    tn: int
    fn: int
    tpr: float
    fpr: float
    precision: float
    recall: float


def divide(a: float, b: float) -> float:
    if b == 0:
        return 0.0
    return a / b


def evaluate_threshold(y_true: list[int], scores: list[float], threshold: float) -> ThresholdResult:
    y_pred = [1 if score >= threshold else 0 for score in scores]

    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)
    tn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 0)
    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)

    tpr = divide(tp, tp + fn)
    fpr = divide(fp, fp + tn)
    precision = divide(tp, tp + fp)
    recall = tpr

    return ThresholdResult(
        threshold=threshold,
        tp=tp,
        fp=fp,
        tn=tn,
        fn=fn,
        tpr=tpr,
        fpr=fpr,
        precision=precision,
        recall=recall,
    )


def evaluate_thresholds(y_true: list[int], scores: list[float], thresholds: list[float]) -> list[ThresholdResult]:
    return [evaluate_threshold(y_true, scores, threshold) for threshold in thresholds]
