from learn_ai_evaluation.rag_metrics import (
    answerability_accuracy,
    average_precision,
    citation_precision,
    claim_support_rate,
    mean_reciprocal_rank,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
    token_f1,
)


def test_retrieval_metrics() -> None:
    relevance = [1, 0, 1, 0]
    assert precision_at_k(relevance, 2) == 0.5
    assert recall_at_k(relevance, total_relevant=2, k=3) == 1.0
    assert reciprocal_rank(relevance) == 1.0
    assert round(average_precision(relevance, total_relevant=2), 6) == round((1.0 + 2 / 3) / 2, 6)


def test_mean_reciprocal_rank() -> None:
    value = mean_reciprocal_rank([[1, 0], [0, 1], [0, 0]])
    assert round(value, 6) == round((1.0 + 0.5 + 0.0) / 3, 6)


def test_answer_metrics() -> None:
    assert token_f1("a correct answer", "a correct answer") == 1.0
    assert claim_support_rate(4, 5) == 0.8
    assert citation_precision(3, 4) == 0.75
    assert answerability_accuracy([True, False], [True, False]) == 1.0


def test_invalid_inputs() -> None:
    import pytest

    with pytest.raises(ValueError):
        precision_at_k([1, 0], 0)
    with pytest.raises(ValueError):
        recall_at_k([1], total_relevant=0, k=1)
    with pytest.raises(ValueError):
        claim_support_rate(2, 1)
    with pytest.raises(ValueError):
        answerability_accuracy([True], [True, False])
