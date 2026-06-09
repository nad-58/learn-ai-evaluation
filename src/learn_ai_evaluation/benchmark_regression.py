"""Benchmark aggregation and regression checks for repository examples."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping


@dataclass(frozen=True)
class RegressionRule:
    """Acceptance rule for one benchmark track."""

    track: str
    baseline_score: float
    minimum_score: float
    max_allowed_drop: float


@dataclass(frozen=True)
class RegressionResult:
    """Regression result for one benchmark track."""

    track: str
    current_score: float
    baseline_score: float
    minimum_score: float
    allowed_floor: float
    delta: float
    passed: bool
    reason: str


def load_benchmark_scores(path: str | Path) -> dict[str, list[float]]:
    """Load per-case scores grouped by track from a CSV file."""
    grouped: dict[str, list[float]] = {}
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"track", "score"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("benchmark CSV must contain track and score columns")
        for row in reader:
            track = row["track"].strip()
            if not track:
                raise ValueError("benchmark track must not be empty")
            grouped.setdefault(track, []).append(float(row["score"]))
    if not grouped:
        raise ValueError("benchmark CSV contains no score rows")
    return grouped


def aggregate_track_scores(grouped: Mapping[str, Iterable[float]]) -> dict[str, float]:
    """Calculate mean score for every track and an equal-weight overall mean."""
    means: dict[str, float] = {}
    for track, values_iter in grouped.items():
        values = [float(value) for value in values_iter]
        if not values:
            raise ValueError(f"track {track!r} has no scores")
        means[track] = sum(values) / len(values)
    means["overall"] = sum(means.values()) / len(means)
    return means


def load_regression_rules(path: str | Path) -> dict[str, RegressionRule]:
    """Load regression rules from CSV."""
    rules: dict[str, RegressionRule] = {}
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {
            "track",
            "baseline_score",
            "minimum_score",
            "max_allowed_drop",
        }
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("baseline CSV is missing required columns")
        for row in reader:
            track = row["track"].strip()
            rules[track] = RegressionRule(
                track=track,
                baseline_score=float(row["baseline_score"]),
                minimum_score=float(row["minimum_score"]),
                max_allowed_drop=float(row["max_allowed_drop"]),
            )
    if not rules:
        raise ValueError("baseline CSV contains no rules")
    return rules


def evaluate_regressions(
    current_scores: Mapping[str, float],
    rules: Mapping[str, RegressionRule],
) -> list[RegressionResult]:
    """Evaluate current scores against absolute and relative regression limits."""
    results: list[RegressionResult] = []
    missing = sorted(set(rules) - set(current_scores))
    if missing:
        raise ValueError(f"missing benchmark scores for: {', '.join(missing)}")

    for track in sorted(rules):
        rule = rules[track]
        current = float(current_scores[track])
        allowed_floor = max(rule.minimum_score, rule.baseline_score - rule.max_allowed_drop)
        passed = current >= allowed_floor
        if passed:
            reason = "within acceptance limits"
        elif current < rule.minimum_score:
            reason = "below minimum score"
        else:
            reason = "drop from baseline exceeds allowed limit"
        results.append(
            RegressionResult(
                track=track,
                current_score=current,
                baseline_score=rule.baseline_score,
                minimum_score=rule.minimum_score,
                allowed_floor=allowed_floor,
                delta=current - rule.baseline_score,
                passed=passed,
                reason=reason,
            )
        )
    return results


def all_passed(results: Iterable[RegressionResult]) -> bool:
    """Return True only when all regression checks pass."""
    values = list(results)
    return bool(values) and all(item.passed for item in values)
