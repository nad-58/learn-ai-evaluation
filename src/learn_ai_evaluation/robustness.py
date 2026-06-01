"""Simple robustness evaluation utilities."""

from __future__ import annotations


def performance_drop(baseline_score: float, changed_input_score: float) -> float:
    return baseline_score - changed_input_score


def robustness_decision(
    baseline_score: float,
    changed_input_score: float,
    allowed_drop: float,
) -> dict:
    drop = performance_drop(baseline_score, changed_input_score)
    return {
        "baseline_score": baseline_score,
        "changed_input_score": changed_input_score,
        "drop": drop,
        "allowed_drop": allowed_drop,
        "passed": drop <= allowed_drop,
    }
