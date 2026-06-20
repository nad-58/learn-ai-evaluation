"""Lightweight scoring utilities for agentic AI risk and governance controls."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

AUTONOMY_DIMENSIONS = (
    "underspecification",
    "long_term_planning",
    "goal_directedness",
    "directedness_of_impact",
    "autonomous_action",
)

CONTROL_DIMENSIONS = (
    "interruptibility",
    "human_approval_triggers",
    "confidential_data_treatment",
    "risk_based_permissions",
    "auditability",
    "monitoring_and_evaluation",
    "model_layer_guardrails",
    "orchestration_layer_guardrails",
    "tool_layer_guardrails",
    "accountability_owner",
)

RISK_TIERS = (
    (0.0, 1.49, "low"),
    (1.5, 2.49, "moderate"),
    (2.5, 3.49, "high"),
    (3.5, 5.0, "critical"),
)


@dataclass(frozen=True)
class AgenticRiskResult:
    autonomy_score: float
    control_score: float
    residual_score: float
    risk_tier: str
    missing_controls: tuple[str, ...]
    recommended_actions: tuple[str, ...]


def _validate_scores(scores: Mapping[str, int | float], expected: tuple[str, ...], name: str) -> None:
    missing = set(expected) - set(scores)
    if missing:
        raise ValueError(f"{name} missing scores for: {sorted(missing)}")
    for key in expected:
        value = scores[key]
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"{name}.{key} must be numeric")
        if not 0 <= float(value) <= 5:
            raise ValueError(f"{name}.{key} must be between 0 and 5")


def _tier(score: float) -> str:
    for low, high, label in RISK_TIERS:
        if low <= score <= high:
            return label
    return "critical"


def _recommend(missing_controls: tuple[str, ...], residual_score: float) -> tuple[str, ...]:
    actions: list[str] = []
    if "interruptibility" in missing_controls:
        actions.append("Add request-level and system-level interrupt or kill-switch controls.")
    if "human_approval_triggers" in missing_controls:
        actions.append("Define approval gates for high-impact or irreversible actions.")
    if "tool_layer_guardrails" in missing_controls or "risk_based_permissions" in missing_controls:
        actions.append("Restrict tools using role-based access and explicit action allow/deny lists.")
    if "orchestration_layer_guardrails" in missing_controls:
        actions.append("Add loop detection, step budgets, timeout limits, and retry ceilings.")
    if "auditability" in missing_controls:
        actions.append("Log goals, prompts, tool calls, observations, decisions, and approvals.")
    if "monitoring_and_evaluation" in missing_controls:
        actions.append("Add continuous monitoring and automated checks for hallucination, policy drift, and compliance failures.")
    if "accountability_owner" in missing_controls:
        actions.append("Assign named operational, compliance, and harm-response owners.")
    if residual_score >= 3.5:
        actions.append("Do not deploy autonomously until critical controls are implemented and red-team findings are closed.")
    return tuple(dict.fromkeys(actions))


def assess_agentic_risk(
    autonomy_scores: Mapping[str, int | float],
    control_scores: Mapping[str, int | float],
    minimum_control_score: float = 3.0,
) -> AgenticRiskResult:
    """Score residual risk for an agentic AI workflow.

    Scores use a 0 to 5 scale. Autonomy scores represent exposure. Control scores
    represent mitigation maturity. The residual score is intentionally simple and
    transparent: mean autonomy exposure minus half of mean control maturity.
    """
    _validate_scores(autonomy_scores, AUTONOMY_DIMENSIONS, "autonomy_scores")
    _validate_scores(control_scores, CONTROL_DIMENSIONS, "control_scores")
    if not 0 <= minimum_control_score <= 5:
        raise ValueError("minimum_control_score must be between 0 and 5")

    autonomy_score = sum(float(autonomy_scores[k]) for k in AUTONOMY_DIMENSIONS) / len(AUTONOMY_DIMENSIONS)
    control_score = sum(float(control_scores[k]) for k in CONTROL_DIMENSIONS) / len(CONTROL_DIMENSIONS)
    residual_score = max(0.0, min(5.0, autonomy_score - 0.5 * control_score))
    missing_controls = tuple(k for k in CONTROL_DIMENSIONS if float(control_scores[k]) < minimum_control_score)
    return AgenticRiskResult(
        autonomy_score=round(autonomy_score, 3),
        control_score=round(control_score, 3),
        residual_score=round(residual_score, 3),
        risk_tier=_tier(residual_score),
        missing_controls=missing_controls,
        recommended_actions=_recommend(missing_controls, residual_score),
    )


def agentic_governance_readiness(result: AgenticRiskResult) -> bool:
    """Return True when the workflow is ready for controlled pilot deployment."""
    return result.risk_tier in {"low", "moderate"} and not result.missing_controls
