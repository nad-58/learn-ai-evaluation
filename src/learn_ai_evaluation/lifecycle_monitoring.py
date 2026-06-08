"""Monitoring and lifecycle evaluation utilities.

This module provides public-safe, domain-neutral helpers for comparing a
reference period with a current monitoring period. It supports feature drift,
performance drift, alert evaluation, and re-evaluation decisions.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, log_loss, roc_auc_score


def population_stability_index(reference: Iterable[float], current: Iterable[float], bins: int = 10) -> float:
    """Calculate PSI using quantile bins derived from the reference sample."""
    ref = np.asarray(reference, dtype=float)
    cur = np.asarray(current, dtype=float)
    if ref.ndim != 1 or cur.ndim != 1:
        raise ValueError("reference and current must be one-dimensional")
    if len(ref) == 0 or len(cur) == 0:
        raise ValueError("reference and current must not be empty")
    if bins < 2:
        raise ValueError("bins must be at least 2")

    edges = np.unique(np.quantile(ref, np.linspace(0, 1, bins + 1)))
    if len(edges) < 3:
        return 0.0
    edges[0], edges[-1] = -np.inf, np.inf
    ref_counts, _ = np.histogram(ref, bins=edges)
    cur_counts, _ = np.histogram(cur, bins=edges)
    eps = 1e-8
    ref_prop = np.clip(ref_counts / len(ref), eps, None)
    cur_prop = np.clip(cur_counts / len(cur), eps, None)
    return float(np.sum((cur_prop - ref_prop) * np.log(cur_prop / ref_prop)))


def numeric_drift_report(reference: pd.DataFrame, current: pd.DataFrame, bins: int = 10) -> pd.DataFrame:
    """Create a feature-level drift report for shared numeric columns."""
    columns = sorted(set(reference.select_dtypes(include=np.number)) & set(current.select_dtypes(include=np.number)))
    rows = []
    for column in columns:
        ref = reference[column].dropna().to_numpy()
        cur = current[column].dropna().to_numpy()
        rows.append({
            "feature": column,
            "reference_n": len(ref),
            "current_n": len(cur),
            "reference_mean": float(np.mean(ref)) if len(ref) else np.nan,
            "current_mean": float(np.mean(cur)) if len(cur) else np.nan,
            "mean_change": float(np.mean(cur) - np.mean(ref)) if len(ref) and len(cur) else np.nan,
            "psi": population_stability_index(ref, cur, bins) if len(ref) and len(cur) else np.nan,
            "missing_rate_reference": float(reference[column].isna().mean()),
            "missing_rate_current": float(current[column].isna().mean()),
        })
    return pd.DataFrame(rows)


def classification_performance(y_true: Iterable[int], y_score: Iterable[float], threshold: float = 0.5) -> dict[str, float]:
    """Calculate common monitoring metrics for binary classification."""
    y = np.asarray(y_true, dtype=int)
    score = np.asarray(y_score, dtype=float)
    if len(y) != len(score):
        raise ValueError("y_true and y_score must have the same length")
    pred = (score >= threshold).astype(int)
    auc = float(roc_auc_score(y, score)) if np.unique(y).size == 2 else np.nan
    return {
        "n": int(len(y)),
        "accuracy": float(accuracy_score(y, pred)),
        "f1": float(f1_score(y, pred, zero_division=0)),
        "auroc": auc,
        "log_loss": float(log_loss(y, np.column_stack([1 - score, score]), labels=[0, 1])),
        "positive_rate": float(np.mean(pred)),
        "outcome_rate": float(np.mean(y)),
    }


def compare_performance(reference_metrics: Mapping[str, float], current_metrics: Mapping[str, float]) -> pd.DataFrame:
    """Compare shared metrics between reference and current periods."""
    rows = []
    for metric in sorted(set(reference_metrics) & set(current_metrics)):
        ref = reference_metrics[metric]
        cur = current_metrics[metric]
        if isinstance(ref, (int, float, np.number)) and isinstance(cur, (int, float, np.number)):
            rows.append({"metric": metric, "reference": ref, "current": cur, "change": cur - ref})
    return pd.DataFrame(rows)


@dataclass(frozen=True)
class AlertRule:
    """A simple threshold rule for lifecycle monitoring."""

    name: str
    field: str
    operator: str
    limit: float
    severity: str = "review"
    action: str = "Investigate and document"


def evaluate_alerts(observations: Mapping[str, float], rules: Iterable[AlertRule]) -> pd.DataFrame:
    """Evaluate observations against predefined monitoring rules."""
    operators = {
        ">": lambda x, y: x > y,
        ">=": lambda x, y: x >= y,
        "<": lambda x, y: x < y,
        "<=": lambda x, y: x <= y,
    }
    rows = []
    for rule in rules:
        if rule.operator not in operators:
            raise ValueError(f"Unsupported operator: {rule.operator}")
        value = observations.get(rule.field, np.nan)
        triggered = bool(np.isfinite(value) and operators[rule.operator](value, rule.limit))
        rows.append({
            "rule": rule.name,
            "field": rule.field,
            "observed": value,
            "operator": rule.operator,
            "limit": rule.limit,
            "triggered": triggered,
            "severity": rule.severity,
            "action": rule.action,
        })
    return pd.DataFrame(rows)


def lifecycle_decision(alert_results: pd.DataFrame) -> str:
    """Return a simple lifecycle decision from triggered alert severities."""
    triggered = alert_results[alert_results["triggered"]]
    if triggered.empty:
        return "continue_monitoring"
    severities = set(triggered["severity"].astype(str).str.lower())
    if "stop" in severities:
        return "pause_and_investigate"
    if "revalidate" in severities:
        return "formal_re_evaluation"
    return "investigate_and_monitor"
