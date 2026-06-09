import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.advanced_ai import (  # noqa: E402
    AgentStep,
    agent_trace_metrics,
    aggregate_scores,
    answer_contains_required_facts,
    citation_coverage,
    groundedness_score,
    lexical_overlap,
    refusal_or_uncertainty_rate,
    retrieval_metrics,
    token_set,
    vlm_answer_score,
)


def test_token_set_normalises_text():
    assert token_set("Hello, HELLO world!") == {"hello", "world"}


def test_lexical_overlap_handles_partial_match():
    score = lexical_overlap("model monitoring baseline", "model baseline review")
    assert 0 < score < 1


def test_answer_contains_required_facts():
    result = answer_contains_required_facts(
        "The answer includes groundedness and citation coverage.",
        ["groundedness", "citation coverage", "latency"],
    )
    assert result["required_fact_hits"] == 2.0
    assert result["required_fact_rate"] == 2 / 3


def test_refusal_or_uncertainty_rate():
    answers = ["The result is supported.", "I do not know based on the evidence."]
    assert refusal_or_uncertainty_rate(answers) == 0.5


def test_retrieval_metrics():
    result = retrieval_metrics(["a", "b", "c"], ["b", "d"], k=2)
    assert result["precision_at_k"] == 0.5
    assert result["recall_at_k"] == 0.5
    assert result["hit_at_k"] == 1.0


def test_groundedness_and_citation_coverage():
    answer = "Monitoring compares current behaviour with a baseline [doc1]."
    contexts = ["Current behaviour can be compared with a baseline."]
    assert groundedness_score(answer, contexts) > 0
    assert citation_coverage(answer, ["[doc1]"]) == 1.0


def test_vlm_answer_score_penalises_forbidden_terms():
    result = vlm_answer_score(
        "The image shows a dashboard and a cat.",
        expected_terms=["dashboard"],
        forbidden_terms=["cat"],
    )
    assert result["expected_term_rate"] == 1.0
    assert result["forbidden_term_hits"] == 1.0
    assert result["vlm_score"] == 0.75


def test_agent_trace_metrics():
    steps = [
        AgentStep(1, "search", "search", True),
        AgentStep(2, "read", "read", True),
        AgentStep(3, "summarise", "summarise", False),
    ]
    result = agent_trace_metrics(steps)
    assert result["action_match_rate"] == 1.0
    assert result["step_success_rate"] == 2 / 3
    assert result["task_success"] == 0.0


def test_aggregate_scores_returns_mean_values():
    frame = aggregate_scores([
        {"groundedness": 0.8, "citation_coverage": 1.0},
        {"groundedness": 0.6, "citation_coverage": 0.5},
    ])
    values = dict(zip(frame["metric"], frame["mean"]))
    assert values["groundedness"] == 0.7
    assert values["citation_coverage"] == 0.75
