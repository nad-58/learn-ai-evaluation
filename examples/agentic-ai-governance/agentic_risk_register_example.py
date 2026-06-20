from learn_ai_evaluation.agentic_risk import assess_agentic_risk


def main():
    autonomy = {
        "underspecification": 4,
        "long_term_planning": 4,
        "goal_directedness": 5,
        "directedness_of_impact": 4,
        "autonomous_action": 4,
    }
    controls = {
        "interruptibility": 2,
        "human_approval_triggers": 2,
        "confidential_data_treatment": 3,
        "risk_based_permissions": 2,
        "auditability": 3,
        "monitoring_and_evaluation": 2,
        "model_layer_guardrails": 3,
        "orchestration_layer_guardrails": 1,
        "tool_layer_guardrails": 2,
        "accountability_owner": 3,
    }
    result = assess_agentic_risk(autonomy, controls)
    print(result)


if __name__ == "__main__":
    main()
