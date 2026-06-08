"""Monitoring and lifecycle evaluation utilities for AI systems."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Optional, Sequence

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score


@dataclass(frozen=True)
class ThresholdRule:
    """Threshold rule used for monitoring checks."""

    metric: str
    warning: float
    action: float
    direction: str = "lower_is_worse"

    def evaluate(self, value: float) -> str:
        if self.direction not in {"lower_is_worse", "higher_is_worse"}:
            raise ValueError("direction must be lower_is_worse or higher_is_worse")
        if self.direction == "lower_is_worse":
            if value <= self.action:
                return "action_required"
            if value <= self.warning:
                return "warning"
            return "pass"
        if value >= self.action:
            return "action_required"
        if value >= self.warning:
            return "warning"
        return "pass"


def binary_classification_metrics(y_true: Sequence[int], y_score: Sequence[float], threshold: float = 0.5) -> Dict[str, float]:
    """Compute common binary classification metrics for periodic review."""

    y_true_array = np.asarray(y_true)
    y_score_array = np.asarray(y_score)
    y_pred = (y_score_array >= threshold).astype(int)

    metrics: Dict[str, float] = {
        "n": float(len(y_true_array)),
        "prevalence": float(np.mean(y_true_array)),
        "accuracy": float(accuracy_score(y_true_array, y_pred)),
        "precision": float(precision_score(y_true_array, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true_array, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true_array, y_pred, zero_division=0)),
    }
    metrics["auroc"] = float(roc_auc_score(y_true_array, y_score_array)) if len(np.unique(y_true_array)) == 2 else float("nan")
    return metrics


def population_stability_index(reference: Sequence[float], current: Sequence[float], bins: int = 10) -> float:
    """Calculate Population Stability Index for one numeric feature."""

    ref = np.asarray(reference, dtype=float)
    cur = np.asarray(current, dtype=float)
    ref = ref[~np.isnan(ref)]
    cur = cur[~np.isnan(cur)]
    if len(ref) == 0 or len(cur) == 0:
        return float("nan")

    edges = np.unique(np.quantile(ref, np.linspace(0, 1, bins + 1)))
    if len(edges) < 2:
        return 0.0

    ref_counts, _ = np.histogram(ref, bins=edges)
    cur_counts, _ = np.histogram(cur, bins=edges)
    epsilon = 1e-6
    ref_pct = np.maximum(ref_counts / max(ref_counts.sum(), 1), epsilon)
    cur_pct = np.maximum(cur_counts / max(cur_counts.sum(), 1), epsilon)
    return float(np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)))


def feature_drift_report(reference_df: pd.DataFrame, current_df: pd.DataFrame, feature_columns: Iterable[str], bins: int = 10) -> pd.DataFrame:
    """Create a feature-level drift report using PSI."""

    rows: List[Dict[str, float | str]] = []
    for feature in feature_columns:
        psi = population_stability_index(reference_df[feature], current_df[feature], bins=bins)
        rows.append({"feature": feature, "psi": psi, "drift_flag": "review" if psi >= 0.2 else "monitor"})
    return pd.DataFrame(rows).sort_values("psi", ascending=False).reset_index(drop=True)


def evaluate_threshold_rules(metrics: Mapping[str, float], rules: Iterable[ThresholdRule]) -> pd.DataFrame:
    """Evaluate metric values against warning and action thresholds."""

    rows: List[Dict[str, float | str]] = []
    for rule in rules:
        value = float(metrics.get(rule.metric, np.nan))
        status = "not_available" if np.isnan(value) else rule.evaluate(value)
        rows.append({
            "metric": rule.metric,
            "value": value,
            "warning_threshold": rule.warning,
            "action_threshold": rule.action,
            "direction": rule.direction,
            "status": status,
        })
    return pd.DataFrame(rows)


def lifecycle_decision(rule_results: pd.DataFrame, drift_report: Optional[pd.DataFrame] = None) -> str:
    """Return a simple lifecycle decision from monitoring outputs."""

    if (rule_results["status"] == "action_required").any():
        return "re_evaluation_or_mitigation_required"
    if drift_report is not None and (drift_report["drift_flag"] == "review").any():
        return "data_shift_review_required"
    if (rule_results["status"] == "warning").any():
        return "increased_monitoring_required"
    return "continue_routine_monitoring"
