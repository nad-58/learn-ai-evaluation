"""Worked example for monitoring and lifecycle evaluation."""
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.monitoring_lifecycle import (  # noqa: E402
    ThresholdRule,
    binary_classification_metrics,
    evaluate_threshold_rules,
    feature_drift_report,
    lifecycle_decision,
)

rng = np.random.default_rng(21)
X_array, y = make_classification(
    n_samples=1400,
    n_features=6,
    n_informative=4,
    n_redundant=1,
    class_sep=1.1,
    weights=[0.62, 0.38],
    random_state=21,
)
feature_names = [f"feature_{i}" for i in range(X_array.shape[1])]
X = pd.DataFrame(X_array, columns=feature_names)

X_train, X_reference, y_train, y_reference = train_test_split(
    X,
    y,
    test_size=0.35,
    stratify=y,
    random_state=21,
)

model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
reference_scores = model.predict_proba(X_reference)[:, 1]
reference_metrics = binary_classification_metrics(y_reference, reference_scores)

# Simulate a later monitoring window where the input distribution has changed.
X_current = X_reference.copy()
X_current["feature_0"] = X_current["feature_0"] + rng.normal(0.65, 0.20, len(X_current))
X_current["feature_2"] = X_current["feature_2"] * 1.20
current_scores = np.clip(model.predict_proba(X_current)[:, 1] - 0.03, 0, 1)
current_metrics = binary_classification_metrics(y_reference, current_scores)

rules = [
    ThresholdRule("auroc", warning=0.82, action=0.78, direction="lower_is_worse"),
    ThresholdRule("recall", warning=0.72, action=0.68, direction="lower_is_worse"),
    ThresholdRule("precision", warning=0.70, action=0.65, direction="lower_is_worse"),
]

rule_results = evaluate_threshold_rules(current_metrics, rules)
drift_report = feature_drift_report(
    reference_df=X_reference,
    current_df=X_current,
    feature_columns=["feature_0", "feature_1", "feature_2", "feature_3"],
)

decision = lifecycle_decision(rule_results, drift_report)

print("\nREFERENCE WINDOW METRICS")
print(pd.Series(reference_metrics).round(3).to_string())

print("\nCURRENT MONITORING WINDOW METRICS")
print(pd.Series(current_metrics).round(3).to_string())

print("\nTHRESHOLD CHECKS")
print(rule_results.round(3).to_string(index=False))

print("\nFEATURE DRIFT REPORT")
print(drift_report.round(3).to_string(index=False))

print("\nLIFECYCLE DECISION")
print(decision)
