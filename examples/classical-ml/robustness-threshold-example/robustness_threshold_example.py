"""Example: threshold-based robustness decision."""

from learn_ai_evaluation.robustness import robustness_decision


def print_result(name: str, result: dict) -> None:
    print(name)
    for key, value in result.items():
        print(f"  {key}: {value}")


def main():
    baseline_accuracy = 0.95
    allowed_drop = 0.05

    scenario_1 = robustness_decision(
        baseline_score=baseline_accuracy,
        changed_input_score=0.91,
        allowed_drop=allowed_drop,
    )

    scenario_2 = robustness_decision(
        baseline_score=baseline_accuracy,
        changed_input_score=0.80,
        allowed_drop=allowed_drop,
    )

    print_result("Scenario 1", scenario_1)
    print()
    print_result("Scenario 2", scenario_2)


if __name__ == "__main__":
    main()
