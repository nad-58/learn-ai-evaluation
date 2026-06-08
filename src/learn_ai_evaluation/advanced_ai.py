"""Utilities for advanced AI evaluation.

The functions are lightweight and educational. They cover LLM output quality,
retrieval quality, groundedness, vision-language answers, and simple agent traces.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Sequence

import numpy as np
import pandas as pd


def token_set(text: str) -> set[str]:
    """Return a simple lower-case token set."""
    cleaned = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
    return {tok for tok in cleaned.split() if tok}


def lexical_overlap(reference: str, prediction: str) -> float:
    """Jaccard overlap between reference and prediction tokens."""
    ref = token_set(reference)
    pred = token_set(prediction)
    if not ref and not pred:
        return 1.0
    if not ref or not pred:
        return 0.0
    return len(ref & pred) / len(ref | pred)


def answer_contains_required_facts(answer: str, required_facts: Sequence[str]) -> Dict[str, float]:
    """Score whether an answer contains required facts or phrases."""
    answer_lower = answer.lower()
    hits = sum(1 for fact in required_facts if fact.lower() in answer_lower)
    total = len(required_facts)
    return {"required_fact_hits": float(hits), "required_fact_total": float(total), "required_fact_rate": hits / total if total else 1.0}


def refusal_or_uncertainty_rate(answers: Sequence[str]) -> float:
    """Estimate how often outputs express uncertainty or refusal."""
    cues = ["i do not know", "i don't know", "not enough information", "cannot determine", "uncertain", "insufficient"]
    count = 0
    for answer in answers:
        low = answer.lower()
        if any(cue in low for cue in cues):
            count += 1
    return count / len(answers) if answers else 0.0


def retrieval_metrics(retrieved_ids: Sequence[str], relevant_ids: Sequence[str], k: int = 5) -> Dict[str, float]:
    """Compute precision@k, recall@k, and hit@k for retrieved document ids."""
    retrieved_at_k = list(retrieved_ids)[:k]
    relevant = set(relevant_ids)
    hits = sum(1 for item in retrieved_at_k if item in relevant)
    return {
        "precision_at_k": hits / k if k else 0.0,
        "recall_at_k": hits / len(relevant) if relevant else 1.0,
        "hit_at_k": 1.0 if hits > 0 else 0.0,
    }


def groundedness_score(answer: str, contexts: Sequence[str]) -> float:
    """Approximate grounding by token overlap between answer and retrieved contexts."""
    context_tokens = token_set(" ".join(contexts))
    answer_tokens = token_set(answer)
    if not answer_tokens:
        return 0.0
    return len(answer_tokens & context_tokens) / len(answer_tokens)


def citation_coverage(answer: str, citation_markers: Sequence[str]) -> float:
    """Measure whether expected citation markers appear in an answer."""
    if not citation_markers:
        return 1.0
    answer_lower = answer.lower()
    hits = sum(1 for marker in citation_markers if marker.lower() in answer_lower)
    return hits / len(citation_markers)


def vlm_answer_score(answer: str, expected_terms: Sequence[str], forbidden_terms: Sequence[str] = ()) -> Dict[str, float]:
    """Simple score for vision-language answers using expected and forbidden terms."""
    answer_lower = answer.lower()
    expected_hits = sum(1 for term in expected_terms if term.lower() in answer_lower)
    forbidden_hits = sum(1 for term in forbidden_terms if term.lower() in answer_lower)
    return {
        "expected_term_rate": expected_hits / len(expected_terms) if expected_terms else 1.0,
        "forbidden_term_hits": float(forbidden_hits),
        "vlm_score": (expected_hits / len(expected_terms) if expected_terms else 1.0) - 0.25 * forbidden_hits,
    }


@dataclass(frozen=True)
class AgentStep:
    """One step in an agent trace."""

    step_id: int
    action: str
    expected_action: str
    success: bool


def agent_trace_metrics(steps: Sequence[AgentStep]) -> Dict[str, float]:
    """Evaluate a simple agent trace."""
    if not steps:
        return {"steps": 0.0, "action_match_rate": 0.0, "step_success_rate": 0.0, "task_success": 0.0}
    action_matches = sum(1 for step in steps if step.action == step.expected_action)
    successes = sum(1 for step in steps if step.success)
    return {
        "steps": float(len(steps)),
        "action_match_rate": action_matches / len(steps),
        "step_success_rate": successes / len(steps),
        "task_success": 1.0 if successes == len(steps) else 0.0,
    }


def aggregate_scores(rows: Iterable[Mapping[str, float]]) -> pd.DataFrame:
    """Aggregate a list of metric dictionaries into mean values."""
    frame = pd.DataFrame(list(rows))
    if frame.empty:
        return pd.DataFrame(columns=["metric", "mean"])
    numeric = frame.select_dtypes(include=[np.number])
    return numeric.mean().reset_index().rename(columns={"index": "metric", 0: "mean"})
