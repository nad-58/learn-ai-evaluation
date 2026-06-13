from learn_ai_evaluation.small_vlm_tool_inventory import (
    hard_negative_false_positive_rate,
    schema_validity_rate,
    tool_count_mae,
    tool_name_f1,
    validate_tool_inventory,
)


def _record(relevant=True, tools=None):
    return {
        "scene_type": "workbench" if relevant else "office desk",
        "relevant": relevant,
        "tools": tools or [],
        "safety_observations": [],
        "unknown_items": [],
        "image_quality": {"status": "usable", "notes": "clear image"},
    }


def test_valid_record_passes_schema():
    output = _record(
        tools=[
            {
                "name": "adjustable wrench",
                "count": 1,
                "visible_condition": "good",
                "confidence": 0.96,
            }
        ]
    )
    assert validate_tool_inventory(output) == []
    assert schema_validity_rate([output]) == 1.0


def test_invalid_record_is_rejected():
    output = _record(
        relevant=False,
        tools=[
            {
                "name": "hammer",
                "count": 0,
                "visible_condition": "broken",
                "confidence": 1.2,
            }
        ],
    )
    errors = validate_tool_inventory(output)
    assert errors
    assert schema_validity_rate([output]) == 0.0


def test_tool_name_and_count_metrics():
    reference = _record(
        tools=[
            {"name": "hammer", "count": 1, "visible_condition": "good", "confidence": 1.0},
            {"name": "screwdriver", "count": 2, "visible_condition": "good", "confidence": 1.0},
        ]
    )
    prediction = _record(
        tools=[
            {"name": "hammer", "count": 1, "visible_condition": "good", "confidence": 0.9},
            {"name": "pliers", "count": 1, "visible_condition": "unknown", "confidence": 0.7},
        ]
    )
    assert tool_name_f1(reference, prediction) == 0.5
    assert tool_count_mae(reference, prediction) == 1.0


def test_hard_negative_false_positive_rate():
    clean = _record(relevant=False)
    false_positive = _record(
        relevant=False,
        tools=[
            {"name": "screwdriver", "count": 1, "visible_condition": "unknown", "confidence": 0.55}
        ],
    )
    assert hard_negative_false_positive_rate([clean, false_positive]) == 0.5
