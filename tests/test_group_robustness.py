import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.group_robustness import (  # noqa: E402
    RobustnessScenario,
    add_gaussian_noise,
    binary_metrics,
    evaluate_groups,
    run_robustness_tests,
    summarise_group_gaps,
)


def test_binary_metrics_perfect_predictions():
    result = binary_metrics([0, 0, 1, 1], [0.1, 0.2, 0.8, 0.9])
    assert result["f1"] == 1.0
    assert result["specificity"] == 1.0
    assert result["auroc"] == 1.0


def test_group_results_and_gap_summary():
    frame = evaluate_groups(
        [0, 1, 0, 1, 0, 1, 0, 1],
        [0.1, 0.9, 0.2, 0.8, 0.4, 0.6, 0.7, 0.3],
        ["A", "A", "A", "A", "B", "B", "B", "B"],
        min_group_size=3,
        n_bootstrap=20,
    )
    assert len(frame) == 2
    assert "auroc_gap_from_best" in frame.columns
    summary = summarise_group_gaps(frame)
    assert set(summary["metric"]) == {"auroc", "recall_sensitivity", "f1"}


def test_robustness_runner_returns_baseline_and_scenario():
    X = pd.DataFrame(
        {
            "a": [-2, -1, 1, 2, -1.5, 1.5],
            "b": [0, 0.2, 0.8, 1, 0.1, 0.9],
        }
    )
    y = np.array([0, 0, 1, 1, 0, 1])
    model = LogisticRegression().fit(X, y)
    results = run_robustness_tests(
        model,
        X,
        y,
        [RobustnessScenario("noise", add_gaussian_noise(0.01), "small noise")],
    )
    assert list(results["scenario"]) == ["baseline", "noise"]
    assert "auroc_change" in results.columns
