"""Worked example for systematic LLM evaluation."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.llm_judge import (  # noqa: E402
    agreement_rate,
    choose_best_variant,
    mean_rubric_score,
    order_adjusted_win_rate,
    proxy_metric_warning,
    win_rate,
)


def main() -> None:
    baseline_results = ["loss", "tie", "loss", "win", "loss"]
    candidate_results_first = ["win", "win", "tie", "loss", "win"]
    candidate_results_second = ["win", "tie", "win", "loss", "win"]

    human_labels = ["win", "loss", "tie", "win", "win"]
    evaluator_labels = ["win", "loss", "tie", "loss", "win"]

    rubric = mean_rubric_score(
        [
            {"relevance": 4, "clarity": 5, "usefulness": 4},
            {"relevance": 5, "clarity": 4, "usefulness": 4},
        ]
    )

    variant_scores = {
        "prompt_v1": win_rate(baseline_results),
        "prompt_v2": order_adjusted_win_rate(
            candidate_results_first,
            candidate_results_second,
        ),
    }

    print("PAIRWISE RESULTS")
    for name, score in variant_scores.items():
        print(f"{name}: {score:.3f}")

    print("\nEVALUATOR CALIBRATION")
    print("Agreement with human labels:", round(agreement_rate(human_labels, evaluator_labels), 3))

    print("\nRUBRIC SCORES")
    for dimension, score in rubric.items():
        print(f"{dimension}: {score:.2f}")

    print("\nPROXY METRIC CHECK")
    warning = proxy_metric_warning(
        target_scores=[0.08, 0.23, 0.11],
        proxy_scores=[0.31, 0.35, 0.42],
    )
    print("Proxy moved opposite to target quality:", warning)

    print("\nBEST VARIANT")
    print(choose_best_variant(variant_scores))


if __name__ == "__main__":
    main()
