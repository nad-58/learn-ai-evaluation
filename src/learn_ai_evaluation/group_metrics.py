"""Simple group-level metric utilities."""

from __future__ import annotations


def divide(a: float, b: float) -> float:
    if b == 0:
        return float("nan")
    return a / b


def positive_rate(positive_count: int, total_count: int) -> float:
    return divide(positive_count, total_count)


def true_positive_rate(tp: int, fn: int) -> float:
    return divide(tp, tp + fn)


def false_positive_rate(fp: int, tn: int) -> float:
    return divide(fp, fp + tn)


def rate_ratio(rate_a: float, rate_b: float) -> float:
    return divide(rate_a, rate_b)
