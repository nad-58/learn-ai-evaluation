"""Group performance and robustness evaluation utilities.

The functions in this module are intentionally domain-neutral and operate on
binary classification outputs. They support public, reproducible examples and
can be adapted to other tasks.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Mapping

import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

ArrayLike = Iterable[float] | np.ndarray | pd.Series


def _as_1d(values: ArrayLike, name: str) -> np.ndarray:
    array = np.asarray(values)
    if array.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    return array


def _safe_auc(y_true: np.ndarray, y_score: np.ndarray) -> float:
    return float("nan") if np.unique(y_true).size < 2 else float(roc_auc_score(y_true, y_score))


def _safe_auprc(y_true: np.ndarray, y_score: np.ndarray) -> float:
    return float("nan") if np.unique(y_true).size < 2 else float(average_precision_score(y_true, y_score))


def binary_metrics(y_true: ArrayLike, y_score: ArrayLike, threshold: float = 0.5) -> dict[str, float]:
    """Calculate common binary classification metrics.

    Specificity is the true-negative rate. Brier score is included as a simple
    probability calibration/error measure; lower values are better.
    """
    y_true_arr = _as_1d(y_true, "y_true").astype(int)
    y_score_arr = _as_1d(y_score, "y_score").astype(float)
    if len(y_true_arr) != len(y_score_arr):
        raise ValueError("y_true and y_score must have the same length")
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1")
    if np.any((y_score_arr < 0) | (y_score_arr > 1)):
        raise ValueError("y_score must contain probabilities between 0 and 1")

    y_pred = (y_score_arr >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true_arr, y_pred, labels=[0, 1]).ravel()
    specificity = tn / (tn + fp) if (tn + fp) else float("nan")

    return {
        "n": int(len(y_true_arr)),
        "prevalence": float(np.mean(y_true_arr)),
        "precision": float(precision_score(y_true_arr, y_pred, zero_division=0)),
        "recall_sensitivity": float(recall_score(y_true_arr, y_pred, zero_division=0)),
        "specificity": float(specificity),
        "f1": float(f1_score(y_true_arr, y_pred, zero_division=0)),
        "auroc": _safe_auc(y_true_arr, y_score_arr),
        "auprc": _safe_auprc(y_true_arr, y_score_arr),
        "brier_score": float(brier_score_loss(y_true_arr, y_score_arr)),
        "false_positive_rate": float(fp / (fp + tn)) if (fp + tn) else float("nan"),
        "false_negative_rate": float(fn / (fn + tp)) if (fn + tp) else float("nan"),
    }


def bootstrap_metric_ci(
    y_true: ArrayLike,
    y_score: ArrayLike,
    metric: str = "auroc",
    threshold: float = 0.5,
    n_bootstrap: int = 500,
    confidence: float = 0.95,
    random_state: int = 42,
) -> tuple[float, float]:
    """Estimate a percentile bootstrap confidence interval for one metric."""
    y_true_arr = _as_1d(y_true, "y_true")
    y_score_arr = _as_1d(y_score, "y_score")
    if len(y_true_arr) != len(y_score_arr):
        raise ValueError("y_true and y_score must have the same length")
    if n_bootstrap < 2:
        raise ValueError("n_bootstrap must be at least 2")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")

    rng = np.random.default_rng(random_state)
    estimates: list[float] = []
    for _ in range(n_bootstrap):
        indices = rng.integers(0, len(y_true_arr), len(y_true_arr))
        value = binary_metrics(y_true_arr[indices], y_score_arr[indices], threshold).get(metric)
        if value is not None and np.isfinite(value):
            estimates.append(float(value))
    if not estimates:
        return float("nan"), float("nan")
    alpha = 1 - confidence
    return tuple(float(v) for v in np.quantile(estimates, [alpha / 2, 1 - alpha / 2]))


def evaluate_groups(
    y_true: ArrayLike,
    y_score: ArrayLike,
    groups: Iterable[object],
    *,
    group_name: str = "group",
    threshold: float = 0.5,
    min_group_size: int = 30,
    ci_metrics: tuple[str, ...] = ("auroc", "recall_sensitivity"),
    n_bootstrap: int = 300,
    random_state: int = 42,
) -> pd.DataFrame:
    """Return per-group metrics, confidence intervals, gaps, and reliability flags."""
    y_true_arr = _as_1d(y_true, "y_true")
    y_score_arr = _as_1d(y_score, "y_score")
    group_arr = _as_1d(groups, "groups")
    if not (len(y_true_arr) == len(y_score_arr) == len(group_arr)):
        raise ValueError("y_true, y_score, and groups must have the same length")

    rows: list[dict[str, object]] = []
    for i, value in enumerate(pd.unique(group_arr)):
        mask = group_arr == value
        metrics = binary_metrics(y_true_arr[mask], y_score_arr[mask], threshold)
        row: dict[str, object] = {group_name: value, **metrics}
        row["sample_size_flag"] = "review" if int(metrics["n"]) < min_group_size else "adequate"
        row["class_coverage_flag"] = "adequate" if np.unique(y_true_arr[mask]).size == 2 else "single_class"
        for metric in ci_metrics:
            low, high = bootstrap_metric_ci(
                y_true_arr[mask], y_score_arr[mask], metric, threshold,
                n_bootstrap=n_bootstrap, random_state=random_state + i,
            )
            row[f"{metric}_ci_low"] = low
            row[f"{metric}_ci_high"] = high
        rows.append(row)

    result = pd.DataFrame(rows)
    metric_columns = ["precision", "recall_sensitivity", "specificity", "f1", "auroc", "auprc"]
    for metric in metric_columns:
        valid = result[metric].dropna()
        best = valid.max() if not valid.empty else np.nan
        result[f"{metric}_gap_from_best"] = best - result[metric]
        result[f"{metric}_ratio_to_best"] = result[metric] / best if np.isfinite(best) and best != 0 else np.nan
    return result.sort_values(group_name).reset_index(drop=True)


def summarise_group_gaps(group_results: pd.DataFrame, metrics: tuple[str, ...] = ("auroc", "recall_sensitivity", "f1")) -> pd.DataFrame:
    """Summarise best, worst, absolute gap, and ratio for selected metrics."""
    rows = []
    for metric in metrics:
        values = group_results[metric].dropna()
        if values.empty:
            rows.append({"metric": metric, "best": np.nan, "worst": np.nan, "absolute_gap": np.nan, "worst_to_best_ratio": np.nan})
            continue
        best, worst = float(values.max()), float(values.min())
        rows.append({
            "metric": metric,
            "best": best,
            "worst": worst,
            "absolute_gap": best - worst,
            "worst_to_best_ratio": worst / best if best else np.nan,
        })
    return pd.DataFrame(rows)


@dataclass(frozen=True)
class RobustnessScenario:
    """A named input transformation used by ``run_robustness_tests``."""

    name: str
    transform: Callable[[pd.DataFrame, np.random.Generator], pd.DataFrame]
    description: str = ""


def add_gaussian_noise(scale: float = 0.1, columns: list[str] | None = None) -> Callable[[pd.DataFrame, np.random.Generator], pd.DataFrame]:
    def transform(frame: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
        output = frame.copy()
        selected = columns or list(output.select_dtypes(include=np.number).columns)
        for column in selected:
            output[column] = output[column] + rng.normal(0, scale, len(output))
        return output
    return transform


def inject_missingness(rate: float = 0.1, columns: list[str] | None = None, fill_value: float = 0.0) -> Callable[[pd.DataFrame, np.random.Generator], pd.DataFrame]:
    def transform(frame: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
        output = frame.copy()
        selected = columns or list(output.select_dtypes(include=np.number).columns)
        for column in selected:
            mask = rng.random(len(output)) < rate
            output.loc[mask, column] = np.nan
            output[column] = output[column].fillna(fill_value)
        return output
    return transform


def scale_features(factor: float = 1.1, columns: list[str] | None = None) -> Callable[[pd.DataFrame, np.random.Generator], pd.DataFrame]:
    def transform(frame: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
        del rng
        output = frame.copy()
        selected = columns or list(output.select_dtypes(include=np.number).columns)
        output[selected] = output[selected] * factor
        return output
    return transform


def run_robustness_tests(
    model: object,
    X: pd.DataFrame,
    y_true: ArrayLike,
    scenarios: Iterable[RobustnessScenario],
    *,
    threshold: float = 0.5,
    random_state: int = 42,
    probability_column: int = 1,
) -> pd.DataFrame:
    """Evaluate baseline and perturbed inputs using a model with ``predict_proba``."""
    if not hasattr(model, "predict_proba"):
        raise TypeError("model must implement predict_proba")
    y_true_arr = _as_1d(y_true, "y_true")
    if len(X) != len(y_true_arr):
        raise ValueError("X and y_true must have the same number of rows")

    baseline_score = np.asarray(model.predict_proba(X))[:, probability_column]
    baseline = binary_metrics(y_true_arr, baseline_score, threshold)
    rows: list[dict[str, object]] = [{"scenario": "baseline", "description": "Unmodified evaluation data", **baseline}]

    rng = np.random.default_rng(random_state)
    for scenario in scenarios:
        transformed = scenario.transform(X.copy(), rng)
        score = np.asarray(model.predict_proba(transformed))[:, probability_column]
        metrics = binary_metrics(y_true_arr, score, threshold)
        row: dict[str, object] = {"scenario": scenario.name, "description": scenario.description, **metrics}
        for metric in ("auroc", "auprc", "recall_sensitivity", "specificity", "f1", "brier_score"):
            row[f"{metric}_change"] = float(metrics[metric] - baseline[metric])
        rows.append(row)
    return pd.DataFrame(rows)


def assess_acceptance(
    group_results: pd.DataFrame,
    robustness_results: pd.DataFrame,
    criteria: Mapping[str, float],
) -> pd.DataFrame:
    """Apply example, project-defined acceptance criteria and return decisions.

    Supported keys: minimum_worst_group_auroc, maximum_auroc_gap,
    minimum_group_size, maximum_robustness_auroc_drop.
    """
    checks: list[dict[str, object]] = []
    worst_auroc = float(group_results["auroc"].min())
    auroc_gap = float(group_results["auroc"].max() - group_results["auroc"].min())
    smallest_group = int(group_results["n"].min())
    perturbed = robustness_results[robustness_results["scenario"] != "baseline"]
    max_drop = float((-perturbed["auroc_change"]).clip(lower=0).max()) if not perturbed.empty else 0.0

    values = {
        "minimum_worst_group_auroc": (worst_auroc, ">="),
        "maximum_auroc_gap": (auroc_gap, "<="),
        "minimum_group_size": (smallest_group, ">="),
        "maximum_robustness_auroc_drop": (max_drop, "<="),
    }
    for name, limit in criteria.items():
        if name not in values:
            raise KeyError(f"Unsupported criterion: {name}")
        observed, operator = values[name]
        passed = observed >= limit if operator == ">=" else observed <= limit
        checks.append({"criterion": name, "operator": operator, "limit": limit, "observed": observed, "decision": "pass" if passed else "review"})
    return pd.DataFrame(checks)
