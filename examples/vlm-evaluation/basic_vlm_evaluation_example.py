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
    mean_rubric_scores,
    recall_at_k,
    token_f1,
    unsupported_claim_rate,
    yes_no_vqa_metrics,
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

    print("SHORT-ANSWER AND RETRIEVAL METRICS")
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

    print("\nOBJECT HALLUCINATION / YES-NO VQA")
    hallucination_metrics = yes_no_vqa_metrics(
        references=[True, False, True, False, False, True],
        predictions=[True, True, True, True, False, True],
    )
    for metric, value in hallucination_metrics.items():
        print(f"{metric}: {value:.3f}")

    print("\nHUMAN OR JUDGE-BASED PLANNING RUBRIC")
    rubric = mean_rubric_scores(
        [
            {
                "object_recognition": 4,
                "spatial_understanding": 3,
                "conciseness": 4,
                "reasonability": 4,
                "executability": 5,
            },
            {
                "object_recognition": 3,
                "spatial_understanding": 4,
                "conciseness": 3,
                "reasonability": 4,
                "executability": 4,
            },
        ]
    )
    for dimension, value in rubric.items():
        print(f"{dimension}: {value:.2f}")


if __name__ == "__main__":
    main()
