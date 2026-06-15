"""Numerical fairness-metric example for two groups.

Run from the repository root:

    python examples/group-performance-and-robustness/fairness_metrics_example.py
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.fairness_metrics import (
    demographic_parity_ratio,
    equalized_odds_gaps,
    fairness_gap_summary,
    group_confusion_rates,
)


def main() -> None:
    # 20 synthetic decisions: 10 in group A and 10 in group B.
    y_true = [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0]
    y_pred = [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0]
    groups = ["A"] * 10 + ["B"] * 10

    rates = group_confusion_rates(y_true, y_pred, groups)
    gaps = fairness_gap_summary(rates)
    parity_ratio = demographic_parity_ratio(rates, "A", "B")
    odds_gaps = equalized_odds_gaps(rates)

    print("PER-GROUP CONFUSION RATES")
    print(rates.round(3).to_string(index=False))

    print("\nFAIRNESS GAP SUMMARY")
    print(gaps.round(3).to_string(index=False))

    print(f"\nDemographic parity ratio B/A: {parity_ratio:.3f}")
    print("Equalized-odds gaps:", {k: round(v, 3) for k, v in odds_gaps.items()})

    print("\nINTERPRETATION")
    print("- Selection rate compares how often each group receives a positive prediction.")
    print("- True-positive-rate gap relates to equality of opportunity.")
    print("- False-positive-rate gap relates to predictive equality.")
    print("- Equalized odds considers both TPR and FPR gaps together.")
    print("- No single fairness metric is universally correct; context and harms matter.")


if __name__ == "__main__":
    main()
