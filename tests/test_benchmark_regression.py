from pathlib import Path

import pytest

from learn_ai_evaluation.benchmark_regression import (
    RegressionRule,
    aggregate_track_scores,
    all_passed,
    evaluate_regressions,
    load_benchmark_scores,
    load_regression_rules,
)


def test_load_and_aggregate_benchmark_scores(tmp_path: Path):
    benchmark = tmp_path / "benchmark.csv"
    benchmark.write_text(
        "track,case_id,score\n"
        "llm,a,0.8\n"
        "llm,b,1.0\n"
        "rag,c,0.6\n",
        encoding="utf-8",
    )

    grouped = load_benchmark_scores(benchmark)
    scores = aggregate_track_scores(grouped)

    assert scores["llm"] == pytest.approx(0.9)
    assert scores["rag"] == pytest.approx(0.6)
    assert scores["overall"] == pytest.approx(0.75)


def test_load_regression_rules(tmp_path: Path):
    baseline = tmp_path / "baseline.csv"
    baseline.write_text(
        "track,baseline_score,minimum_score,max_allowed_drop\n"
        "llm,0.9,0.8,0.05\n",
        encoding="utf-8",
    )

    rules = load_regression_rules(baseline)
    assert rules["llm"] == RegressionRule("llm", 0.9, 0.8, 0.05)


def test_regression_passes_at_allowed_floor():
    rules = {
        "llm": RegressionRule(
            track="llm",
            baseline_score=0.9,
            minimum_score=0.8,
            max_allowed_drop=0.05,
        )
    }
    results = evaluate_regressions({"llm": 0.85}, rules)

    assert results[0].passed is True
    assert results[0].allowed_floor == pytest.approx(0.85)
    assert all_passed(results) is True


def test_regression_fails_when_drop_exceeds_limit():
    rules = {
        "llm": RegressionRule(
            track="llm",
            baseline_score=0.9,
            minimum_score=0.7,
            max_allowed_drop=0.05,
        )
    }
    results = evaluate_regressions({"llm": 0.84}, rules)

    assert results[0].passed is False
    assert results[0].reason == "drop from baseline exceeds allowed limit"
    assert all_passed(results) is False


def test_regression_fails_below_absolute_minimum():
    rules = {
        "rag": RegressionRule(
            track="rag",
            baseline_score=0.6,
            minimum_score=0.55,
            max_allowed_drop=0.2,
        )
    }
    results = evaluate_regressions({"rag": 0.5}, rules)

    assert results[0].passed is False
    assert results[0].reason == "below minimum score"


def test_missing_track_raises_error():
    rules = {
        "agent": RegressionRule("agent", 0.8, 0.7, 0.05),
    }
    with pytest.raises(ValueError, match="missing benchmark scores"):
        evaluate_regressions({"llm": 0.9}, rules)
