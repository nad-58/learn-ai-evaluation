"""Worked example for group performance and robustness evaluation."""
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.group_robustness import (  # noqa: E402
    RobustnessScenario,
    add_gaussian_noise,
    assess_acceptance,
    evaluate_groups,
    inject_missingness,
    run_robustness_tests,
    scale_features,
    summarise_group_gaps,
)

rng = np.random.default_rng(7)
X_array, y = make_classification(
    n_samples=1200,
    n_features=8,
    n_informative=5,
    n_redundant=1,
    weights=[0.65, 0.35],
    class_sep=1.2,
    random_state=7,
)
X = pd.DataFrame(X_array, columns=[f"feature_{i}" for i in range(X_array.shape[1])])
group = rng.choice(
    ["environment_A", "environment_B", "environment_C"],
    size=len(X),
    p=[0.45, 0.35, 0.20],
)

# Introduce a controlled synthetic challenge in one group to show why slicing matters.
X.loc[group == "environment_C", "feature_0"] += rng.normal(
    0, 1.5, np.sum(group == "environment_C")
)

X_train, X_test, y_train, y_test, group_train, group_test = train_test_split(
    X,
    y,
    group,
    test_size=0.35,
    stratify=y,
    random_state=11,
)
model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
y_score = model.predict_proba(X_test)[:, 1]

group_results = evaluate_groups(
    y_test,
    y_score,
    group_test,
    group_name="environment",
    min_group_size=50,
    n_bootstrap=200,
)
print("\nPER-GROUP RESULTS")
print(group_results.round(3).to_string(index=False))

print("\nGAP SUMMARY")
print(summarise_group_gaps(group_results).round(3).to_string(index=False))

scenarios = [
    RobustnessScenario(
        "mild_noise",
        add_gaussian_noise(scale=0.10),
        "Gaussian noise added to numeric features",
    ),
    RobustnessScenario(
        "missing_inputs",
        inject_missingness(rate=0.08, fill_value=0.0),
        "Eight percent missingness with a simple fallback value",
    ),
    RobustnessScenario(
        "feature_scale_shift",
        scale_features(factor=1.15),
        "Numeric features scaled by 15 percent",
    ),
]
robustness_results = run_robustness_tests(model, X_test, y_test, scenarios)
print("\nROBUSTNESS RESULTS")
print(robustness_results.round(3).to_string(index=False))

criteria = {
    "minimum_worst_group_auroc": 0.75,
    "maximum_auroc_gap": 0.12,
    "minimum_group_size": 50,
    "maximum_robustness_auroc_drop": 0.08,
}
print("\nILLUSTRATIVE ACCEPTANCE CHECKS")
print(
    assess_acceptance(group_results, robustness_results, criteria)
    .round(3)
    .to_string(index=False)
)
