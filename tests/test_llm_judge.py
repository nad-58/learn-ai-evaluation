import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.llm_judge import (  # noqa: E402
    agreement_rate,
    choose_best_variant,
    mean_rubric_score,
    order_adjusted_win_rate,
    proxy_metric_warning,
    win_rate,
)


def test_win_rate():
    assert win_rate(["win", "loss", "tie", "win"]) == 0.5


def test_order_adjusted_win_rate():
    first = ["win", "loss", "win", "tie"]
    second = ["win", "win", "loss", "tie"]
    assert order_adjusted_win_rate(first, second) == 0.5


def test_agreement_rate():
    reference = ["win", "loss", "tie", "win"]
    evaluator = ["win", "loss", "loss", "win"]
    assert agreement_rate(reference, evaluator) == 0.75


def test_mean_rubric_score():
    result = mean_rubric_score(
        [
            {"clarity": 4, "usefulness": 5},
            {"clarity": 2, "usefulness": 3},
        ]
    )
    assert result["clarity"] == 3.0
    assert result["usefulness"] == 4.0


def test_proxy_metric_warning():
    assert proxy_metric_warning([0.2, 0.1], [0.3, 0.4]) is True
    assert proxy_metric_warning([0.2, 0.3], [0.3, 0.4]) is False


def test_choose_best_variant():
    assert choose_best_variant({"prompt_a": 0.4, "prompt_b": 0.6}) == "prompt_b"
