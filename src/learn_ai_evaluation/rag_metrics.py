"""Dependency-free educational metrics for retrieval-augmented generation evaluation."""

from collections import Counter
from typing import Iterable, Sequence


def precision_at_k(relevance: Sequence[int], k: int) -> float:
    """Return the fraction of the top-k retrieved items that are relevant."""
    if k < 1:
        raise ValueError("k must be at least 1")
    top_k = list(relevance[:k])
    if not top_k:
        return 0.0
    if any(value not in (0, 1) for value in top_k):
        raise ValueError("relevance values must be 0 or 1")
    return sum(top_k) / len(top_k)


def recall_at_k(relevance: Sequence[int], total_relevant: int, k: int) -> float:
    """Return the fraction of all relevant items found within the top-k results."""
    if k < 1:
        raise ValueError("k must be at least 1")
    if total_relevant < 1:
        raise ValueError("total_relevant must be at least 1")
    top_k = list(relevance[:k])
    if any(value not in (0, 1) for value in top_k):
        raise ValueError("relevance values must be 0 or 1")
    return min(1.0, sum(top_k) / total_relevant)


def reciprocal_rank(relevance: Sequence[int]) -> float:
    """Return the reciprocal rank of the first relevant retrieved item."""
    for rank, value in enumerate(relevance, start=1):
        if value not in (0, 1):
            raise ValueError("relevance values must be 0 or 1")
        if value == 1:
            return 1.0 / rank
    return 0.0


def mean_reciprocal_rank(relevance_lists: Iterable[Sequence[int]]) -> float:
    """Return the mean reciprocal rank across multiple queries."""
    values = [reciprocal_rank(items) for items in relevance_lists]
    return sum(values) / len(values) if values else 0.0


def average_precision(relevance: Sequence[int], total_relevant: int | None = None) -> float:
    """Compute average precision for one ranked retrieval list."""
    if any(value not in (0, 1) for value in relevance):
        raise ValueError("relevance values must be 0 or 1")
    relevant_count = sum(relevance) if total_relevant is None else total_relevant
    if relevant_count < 1:
        return 0.0

    precisions = []
    found = 0
    for rank, value in enumerate(relevance, start=1):
        if value == 1:
            found += 1
            precisions.append(found / rank)
    return sum(precisions) / relevant_count if precisions else 0.0


def token_f1(reference: str, prediction: str) -> float:
    """Compute bag-of-token F1 for answer correctness."""
    ref = reference.lower().split()
    pred = prediction.lower().split()
    if not ref and not pred:
        return 1.0
    if not ref or not pred:
        return 0.0
    overlap = sum((Counter(ref) & Counter(pred)).values())
    if overlap == 0:
        return 0.0
    precision = overlap / len(pred)
    recall = overlap / len(ref)
    return 2 * precision * recall / (precision + recall)


def claim_support_rate(supported_claims: int, total_claims: int) -> float:
    """Return the fraction of generated claims supported by retrieved context."""
    if total_claims < 1:
        raise ValueError("total_claims must be at least 1")
    if supported_claims < 0 or supported_claims > total_claims:
        raise ValueError("supported_claims must be between zero and total_claims")
    return supported_claims / total_claims


def citation_precision(valid_citations: int, total_citations: int) -> float:
    """Return the fraction of citations that correctly support their associated claims."""
    if total_citations < 1:
        raise ValueError("total_citations must be at least 1")
    if valid_citations < 0 or valid_citations > total_citations:
        raise ValueError("valid_citations must be between zero and total_citations")
    return valid_citations / total_citations


def answerability_accuracy(expected_answerable: Iterable[bool], answered: Iterable[bool]) -> float:
    """Measure whether the system answers answerable queries and abstains otherwise."""
    expected = list(expected_answerable)
    observed = list(answered)
    if len(expected) != len(observed):
        raise ValueError("expected_answerable and answered must have the same length")
    if not expected:
        return 0.0
    return sum(a == b for a, b in zip(expected, observed)) / len(expected)
