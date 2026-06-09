"""Lightweight metrics for large vision-language model evaluation."""

from collections import Counter
from typing import Iterable, Mapping, Sequence


def normalize_text(text: str) -> str:
    """Lowercase text, remove punctuation, and normalize whitespace."""
    return " ".join("".join(c if c.isalnum() else " " for c in text.lower()).split())


def exact_match(reference: str, prediction: str) -> float:
    """Return 1.0 when normalized texts match, otherwise 0.0."""
    return float(normalize_text(reference) == normalize_text(prediction))


def token_f1(reference: str, prediction: str) -> float:
    """Compute bag-of-token F1 for short-answer outputs."""
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
    """Compute MRR from one-based relevant-item ranks.

    Use ``None`` when no relevant item was retrieved.
    """
    values: list[float] = []
    for rank in ranks:
        if rank is None:
            values.append(0.0)
        elif rank < 1:
            raise ValueError("ranks must be positive integers or None")
        else:
            values.append(1.0 / rank)
    return sum(values) / len(values) if values else 0.0


def recall_at_k(ranks: Iterable[int | None], k: int) -> float:
    """Return the fraction of relevant items appearing within the top-k results."""
    if k < 1:
        raise ValueError("k must be at least 1")

    values = list(ranks)
    for rank in values:
        if rank is not None and rank < 1:
            raise ValueError("ranks must be positive integers or None")

    return (
        sum(rank is not None and rank <= k for rank in values) / len(values)
        if values
        else 0.0
    )


def unsupported_claim_rate(flags: Iterable[bool]) -> float:
    """Return the proportion of reviewed outputs with unsupported visual claims."""
    values = list(flags)
    return sum(bool(flag) for flag in values) / len(values) if values else 0.0


def abstention_rates(
    answerable: Iterable[bool], abstained: Iterable[bool]
) -> dict[str, float]:
    """Compute appropriate and unnecessary abstention rates.

    ``answerable`` and ``abstained`` must describe the same samples.
    """
    answerable_values = list(answerable)
    abstained_values = list(abstained)
    if len(answerable_values) != len(abstained_values):
        raise ValueError("answerable and abstained must have the same length")

    pairs = list(zip(answerable_values, abstained_values))
    unanswerable = [abstain for can_answer, abstain in pairs if not can_answer]
    answerable_items = [abstain for can_answer, abstain in pairs if can_answer]

    return {
        "appropriate_abstention_rate": (
            sum(unanswerable) / len(unanswerable) if unanswerable else 0.0
        ),
        "unnecessary_abstention_rate": (
            sum(answerable_items) / len(answerable_items) if answerable_items else 0.0
        ),
    }


def yes_no_vqa_metrics(
    references: Sequence[bool], predictions: Sequence[bool]
) -> dict[str, float]:
    """Compute POPE-style metrics for yes/no visual questions.

    ``True`` represents a positive or ``yes`` answer. In addition to accuracy,
    precision, recall, and F1, the function reports the model's overall yes ratio,
    which can reveal a tendency to agree with object-presence questions.
    """
    if len(references) != len(predictions):
        raise ValueError("references and predictions must have the same length")
    if not references:
        return {
            "accuracy": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1": 0.0,
            "yes_ratio": 0.0,
        }

    true_positive = sum(ref and pred for ref, pred in zip(references, predictions))
    true_negative = sum((not ref) and (not pred) for ref, pred in zip(references, predictions))
    false_positive = sum((not ref) and pred for ref, pred in zip(references, predictions))
    false_negative = sum(ref and (not pred) for ref, pred in zip(references, predictions))

    precision = (
        true_positive / (true_positive + false_positive)
        if true_positive + false_positive
        else 0.0
    )
    recall = (
        true_positive / (true_positive + false_negative)
        if true_positive + false_negative
        else 0.0
    )
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    return {
        "accuracy": (true_positive + true_negative) / len(references),
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "yes_ratio": sum(predictions) / len(predictions),
    }


def mean_rubric_scores(
    records: Iterable[Mapping[str, float]],
) -> dict[str, float]:
    """Average rubric dimensions for human or judge-based VLM evaluation.

    Example dimensions include object recognition, spatial understanding,
    conciseness, reasonability, and executability.
    """
    rows = list(records)
    if not rows:
        return {}

    keys = set().union(*(row.keys() for row in rows))
    result: dict[str, float] = {}
    for key in sorted(keys):
        values = [float(row[key]) for row in rows if key in row]
        if values:
            result[key] = sum(values) / len(values)
    return result
