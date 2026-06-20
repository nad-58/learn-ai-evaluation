import pytest

from learn_ai_evaluation.agentic_risk import (
    AUTONOMY_DIMENSIONS,
    CONTROL_DIMENSIONS,
    agentic_governance_readiness,
    assess_agentic_risk,
)


def _scores(keys, value):
    return {key: value for key in keys}


def test_high_autonomy_with_weak_controls_is_not_ready():
    result = assess_agentic_risk(_scores(AUTONOMY_DIMENSIONS, 5), _scores(CONTROL_DIMENSIONS, 1))
    assert result.risk_tier == "critical"
    assert not agentic_governance_readiness(result)
    assert "interruptibility" in result.missing_controls
    assert result.recommended_actions


def test_mature_controls_reduce_residual_risk():
    result = assess_agentic_risk(_scores(AUTONOMY_DIMENSIONS, 3), _scores(CONTROL_DIMENSIONS, 5))
    assert result.risk_tier in {"low", "moderate"}
    assert result.missing_controls == ()
    assert agentic_governance_readiness(result)


def test_missing_dimension_is_rejected():
    autonomy = _scores(AUTONOMY_DIMENSIONS, 3)
    autonomy.pop("underspecification")
    with pytest.raises(ValueError):
        assess_agentic_risk(autonomy, _scores(CONTROL_DIMENSIONS, 3))


def test_out_of_range_score_is_rejected():
    controls = _scores(CONTROL_DIMENSIONS, 3)
    controls["auditability"] = 8
    with pytest.raises(ValueError):
        assess_agentic_risk(_scores(AUTONOMY_DIMENSIONS, 3), controls)
