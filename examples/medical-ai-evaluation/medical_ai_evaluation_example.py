"""Worked example for technical medical AI evaluation using synthetic data.

Run from the repository root:

    python examples/medical-ai-evaluation/medical_ai_evaluation_example.py
"""

from pathlib import Path
from pprint import pprint
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.medical_ai_metrics import (  # noqa: E402
    binary_evaluation,
    dice_score,
    site_level_evaluation,
    threshold_predictions,
    wilson_interval,
)


def main() -> None:
    y_true = [1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0]
    probabilities = [0.91, 0.20, 0.73, 0.48, 0.15, 0.62, 0.88, 0.33, 0.81, 0.12, 0.67, 0.41]
    sites = ["site_a"] * 6 + ["site_b"] * 6

    predictions = threshold_predictions(probabilities, threshold=0.50)
    overall = binary_evaluation(y_true, predictions)

    print("Overall case-level evaluation")
    pprint(overall)

    sensitivity_interval = wilson_interval(
        successes=overall.true_positive,
        total=overall.true_positive + overall.false_negative,
    )
    specificity_interval = wilson_interval(
        successes=overall.true_negative,
        total=overall.true_negative + overall.false_positive,
    )
    print(f"Sensitivity 95% interval: {sensitivity_interval}")
    print(f"Specificity 95% interval: {specificity_interval}")

    print("\nSite-level evaluation")
    for site, result in site_level_evaluation(y_true, predictions, sites).items():
        print(site)
        pprint(result)

    reference_mask = [0, 0, 1, 1, 1, 0, 0, 1]
    predicted_mask = [0, 1, 1, 1, 0, 0, 0, 1]
    print(f"\nSynthetic segmentation Dice score: {dice_score(reference_mask, predicted_mask):.3f}")


if __name__ == "__main__":
    main()
