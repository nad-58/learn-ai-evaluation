"""Utilities for systematic LLM evaluation."""

from __future__ import annotations

from typing import Iterable, Mapping, Sequence


def win_rate(results: Sequence[str]) -> float:
    """Return the fraction of comparisons labelled as a win."""
    if not results:
        return 0.0
    allowed = {"win", "loss", "tie"}
    if any(item not in allowed for item in results):
        raise ValueError("results must contain win, loss, or tie")
    return sum(item == "win" for item in results) / len(results)


def order_adjusted_win_rate(first_order: Sequence[str], second_order: Sequence[str]) -> float:
    """Average win rates after evaluating the same pairs in both orders."""
    if len(first_order) != len(second_order):
        raise ValueError("result lists must have the same length")
    if not first_order:
        return 0.0
    return (win_rate(first_order) + win_rate(second_order)) / 2


def agreement_rate(reference_labels: Sequence[str], evaluator_labels: Sequence[str]) -> float:
    """Return exact agreement between reference and evaluator labels."""
    if len(reference_labels) != len(evaluator_labels):
        raise ValueError("label lists must have the same length")
    if not reference_labels:
        return 0.0
    return sum(a == b for a, b in zip(reference_labels, evaluator_labels)) / len(reference_labels)


def mean_rubric_score(records: Iterable[Mapping[str, float]]) -> dict[str, float]:
    """Average rubric dimensions across evaluated outputs."""
    rows = list(records)
    if not rows:
        return {}
    keys = set().union(*(row.keys() for row in rows))
    result: dict[str, float] = {}
    for key in sorted(keys):
        values = [float(row[key]) for row in rows if key in row]
        result[key] = sum(values) / len(values)
    return result


def proxy_metric_warning(target_scores: Sequence[float], proxy_scores: Sequence[float]) -> bool:
    """Flag when a proxy metric moves opposite to the target quality measure."""
    if len(target_scores) != len(proxy_scores):
        raise ValueError("score lists must have the same length")
    if len(target_scores) < 2:
        return False
    target_change = target_scores[-1] - target_scores[0]
    proxy_change = proxy_scores[-1] - proxy_scores[0]
    return target_change * proxy_change < 0


def choose_best_variant(scores: Mapping[str, float]) -> str:
    """Return the highest-scoring prompt or system variant."""
    if not scores:
        raise ValueError("scores must not be empty")
    return max(scores, key=scores.get)
