"""Lightweight metrics for vision-language model evaluation."""

from collections import Counter
from typing import Iterable


def normalize_text(text: str) -> str:
    return " ".join("".join(c if c.isalnum() else " " for c in text.lower()).split())


def exact_match(reference: str, prediction: str) -> float:
    return float(normalize_text(reference) == normalize_text(prediction))


def token_f1(reference: str, prediction: str) -> float:
    ref = normalize_text(reference).split()
    pred = normalize_text(prediction).split()
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


def mean_reciprocal_rank(ranks: Iterable[int | None]) -> float:
    values = [0.0 if rank is None else 1.0 / rank for rank in ranks]
    return sum(values) / len(values) if values else 0.0


def recall_at_k(ranks: Iterable[int | None], k: int) -> float:
    if k < 1:
        raise ValueError("k must be at least 1")
    values = list(ranks)
    return sum(rank is not None and rank <= k for rank in values) / len(values) if values else 0.0


def unsupported_claim_rate(flags: Iterable[bool]) -> float:
    values = list(flags)
    return sum(bool(flag) for flag in values) / len(values) if values else 0.0


def abstention_rates(answerable: Iterable[bool], abstained: Iterable[bool]) -> dict[str, float]:
    pairs = list(zip(answerable, abstained))
    unanswerable = [abstain for can_answer, abstain in pairs if not can_answer]
    answerable_items = [abstain for can_answer, abstain in pairs if can_answer]
    return {
        "appropriate_abstention_rate": sum(unanswerable) / len(unanswerable) if unanswerable else 0.0,
        "unnecessary_abstention_rate": sum(answerable_items) / len(answerable_items) if answerable_items else 0.0,
    }
