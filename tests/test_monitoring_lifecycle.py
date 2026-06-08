import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.monitoring_lifecycle import (  # noqa: E402
    ThresholdRule,
    binary_classification_metrics,
    evaluate_threshold_rules,
    feature_drift_report,
    lifecycle_decision,
    population_stability_index,
)


def test_threshold_rule_lower_is_worse():
    rule = ThresholdRule("recall", warning=0.75, action=0.70)
    assert rule.evaluate(0.80) == "pass"
    assert rule.evaluate(0.74) == "warning"
    assert rule.evaluate(0.69) == "action_required"


def test_binary_classification_metrics_returns_expected_keys():
    metrics = binary_classification_metrics([0, 0, 1, 1], [0.1, 0.2, 0.8, 0.9])
    assert metrics["accuracy"] == 1.0
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["auroc"] == 1.0


def test_population_stability_index_zero_for_same_distribution():
    values = [1, 2, 3, 4, 5, 6]
    assert population_stability_index(values, values, bins=3) == 0.0


def test_feature_drift_report_and_decision():
    reference = pd.DataFrame({"a": [0, 1, 2, 3, 4, 5], "b": [1, 1, 2, 2, 3, 3]})
    current = pd.DataFrame({"a": [4, 5, 6, 7, 8, 9], "b": [1, 1, 2, 2, 3, 3]})
    drift = feature_drift_report(reference, current, ["a", "b"], bins=3)
    assert set(drift["feature"]) == {"a", "b"}

    rules = [ThresholdRule("auroc", warning=0.80, action=0.75)]
    checks = evaluate_threshold_rules({"auroc": 0.74}, rules)
    assert lifecycle_decision(checks, drift) == "re_evaluation_or_mitigation_required"
