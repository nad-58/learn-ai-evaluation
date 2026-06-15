import pandas as pd
import pytest

from learn_ai_evaluation.fairness_metrics import (
    demographic_parity_ratio,
    equalized_odds_gaps,
    fairness_gap_summary,
    group_confusion_rates,
)


def test_group_confusion_rates():
    rates = group_confusion_rates(
        y_true=[1, 1, 0, 0, 1, 1, 0, 0],
        y_pred=[1, 0, 1, 0, 1, 1, 0, 0],
        groups=["A", "A", "A", "A", "B", "B", "B", "B"],
    )
    assert rates["n"].tolist() == [4, 4]
    assert rates.loc[rates["group"] == "A", "selection_rate"].iloc[0] == pytest.approx(0.5)
    assert rates.loc[rates["group"] == "B", "true_positive_rate"].iloc[0] == pytest.approx(1.0)


def test_fairness_gap_and_ratio():
    rates = pd.DataFrame(
        {
            "group": ["A", "B"],
            "selection_rate": [0.50, 0.40],
            "true_positive_rate": [0.80, 0.60],
            "false_positive_rate": [0.20, 0.10],
            "positive_predictive_value": [0.70, 0.75],
        }
    )
    gaps = fairness_gap_summary(rates)
    assert demographic_parity_ratio(rates, "A", "B") == pytest.approx(0.8)
    assert gaps.loc[gaps["metric"] == "selection_rate", "absolute_gap"].iloc[0] == pytest.approx(0.1)

    odds_gaps = equalized_odds_gaps(rates)
    assert odds_gaps["true_positive_rate_gap"] == pytest.approx(0.2)
    assert odds_gaps["false_positive_rate_gap"] == pytest.approx(0.1)
