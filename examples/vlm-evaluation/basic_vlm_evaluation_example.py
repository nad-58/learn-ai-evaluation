"""Worked example for large vision-language model evaluation.

Run from the repository root:

    python examples/vlm-evaluation/basic_vlm_evaluation_example.py
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.vlm_metrics import (  # noqa: E402
    abstention_rates,
    exact_match,
    mean_reciprocal_rank,
    recall_at_k,
    token_f1,
    unsupported_claim_rate,
)


def main() -> None:
    records = [
        {"reference": "two red cars", "prediction": "Two red cars.", "unsupported": False},
        {"reference": "a dog on grass", "prediction": "a dog outside", "unsupported": False},
        {"reference": "not visible", "prediction": "a blue bicycle", "unsupported": True},
    ]

    exact_scores = [exact_match(r["reference"], r["prediction"]) for r in records]
    f1_scores = [token_f1(r["reference"], r["prediction"]) for r in records]
    ranks = [1, 3, None, 2]

    print("Mean exact match:", round(sum(exact_scores) / len(exact_scores), 3))
    print("Mean token F1:", round(sum(f1_scores) / len(f1_scores), 3))
    print("Retrieval MRR:", round(mean_reciprocal_rank(ranks), 3))
    print("Retrieval Recall@2:", round(recall_at_k(ranks, 2), 3))
    print(
        "Unsupported claim rate:",
        round(unsupported_claim_rate(r["unsupported"] for r in records), 3),
    )
    print(
        "Abstention rates:",
        abstention_rates(
            answerable=[True, True, False, False],
            abstained=[False, False, True, False],
        ),
    )


if __name__ == "__main__":
    main()
