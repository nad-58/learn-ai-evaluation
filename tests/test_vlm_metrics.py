import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.vlm_metrics import (  # noqa: E402
    abstention_rates,
    exact_match,
    mean_reciprocal_rank,
    mean_rubric_scores,
    recall_at_k,
    token_f1,
    unsupported_claim_rate,
    yes_no_vqa_metrics,
)


def test_exact_match_and_token_f1():
    assert exact_match("Two red cars", "two red cars.") == 1.0
    assert 0 < token_f1("a dog on grass", "a dog outside") < 1


def test_retrieval_rank_metrics():
    ranks = [1, 3, None, 2]
    assert mean_reciprocal_rank(ranks) == (1 + 1 / 3 + 0 + 1 / 2) / 4
    assert recall_at_k(ranks, 2) == 0.5


def test_unsupported_claim_rate():
    assert unsupported_claim_rate([False, True, False, True]) == 0.5


def test_abstention_rates():
    result = abstention_rates(
        answerable=[True, True, False, False],
        abstained=[False, True, True, False],
    )
    assert result["appropriate_abstention_rate"] == 0.5
    assert result["unnecessary_abstention_rate"] == 0.5


def test_yes_no_vqa_metrics_reports_yes_bias():
    result = yes_no_vqa_metrics(
        references=[True, False, True, False],
        predictions=[True, True, True, True],
    )
    assert result["accuracy"] == 0.5
    assert result["precision"] == 0.5
    assert result["recall"] == 1.0
    assert result["f1"] == 2 / 3
    assert result["yes_ratio"] == 1.0


def test_mean_rubric_scores():
    scores = mean_rubric_scores(
        [
            {"object_recognition": 4, "spatial": 3, "executability": 5},
            {"object_recognition": 2, "spatial": 5, "executability": 3},
        ]
    )
    assert scores["object_recognition"] == 3.0
    assert scores["spatial"] == 4.0
    assert scores["executability"] == 4.0
