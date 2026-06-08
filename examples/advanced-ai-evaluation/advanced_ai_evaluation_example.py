"""Worked example for Phase 7 advanced AI evaluation."""
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
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
    vlm_answer_score,
)

print("\n1. LARGE LANGUAGE MODEL EVALUATION")
reference = "The system should explain that monitoring compares current performance with a reference baseline."
prediction = "Monitoring compares current model performance with a reference baseline and flags changes over time."
llm_scores = {
    "lexical_overlap": lexical_overlap(reference, prediction),
    **answer_contains_required_facts(prediction, ["reference baseline", "performance", "changes"]),
    "uncertainty_rate": refusal_or_uncertainty_rate([prediction]),
}
print(pd.Series(llm_scores).round(3).to_string())

print("\n2. VISION LANGUAGE MODEL EVALUATION")
vlm_answer = "The image shows a dashboard with a line chart, warning indicators, and a table of model metrics."
vlm_scores = vlm_answer_score(
    answer=vlm_answer,
    expected_terms=["dashboard", "line chart", "warning", "metrics"],
    forbidden_terms=["cat", "car"],
)
print(pd.Series(vlm_scores).round(3).to_string())

print("\n3. RAG EVALUATION")
retrieved = ["doc_monitoring", "doc_dataset", "doc_risk", "doc_ui"]
relevant = ["doc_monitoring", "doc_risk"]
contexts = [
    "Monitoring compares current behaviour with a baseline.",
    "A review can use thresholds, drift checks, and documented findings.",
]
rag_answer = "Monitoring compares current behaviour with a baseline and should include documented findings [doc_monitoring]."
rag_scores = {
    **retrieval_metrics(retrieved, relevant, k=3),
    "groundedness": groundedness_score(rag_answer, contexts),
    "citation_coverage": citation_coverage(rag_answer, ["[doc_monitoring]"]),
}
print(pd.Series(rag_scores).round(3).to_string())

print("\n4. AGENTIC AI EVALUATION")
trace = [
    AgentStep(1, "search", "search", True),
    AgentStep(2, "read", "read", True),
    AgentStep(3, "summarise", "summarise", True),
]
agent_scores = agent_trace_metrics(trace)
print(pd.Series(agent_scores).round(3).to_string())

print("\n5. COMBINED SYSTEM-LEVEL EVALUATION")
combined = aggregate_scores([llm_scores, vlm_scores, rag_scores, agent_scores])
print(combined.round(3).to_string(index=False))
