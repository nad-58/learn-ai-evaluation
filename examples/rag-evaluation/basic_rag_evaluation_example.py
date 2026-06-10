"""Worked example for retrieval-augmented generation evaluation.

Run from the repository root:

    python examples/rag-evaluation/basic_rag_evaluation_example.py
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.rag_metrics import (  # noqa: E402
    answerability_accuracy,
    average_precision,
    citation_precision,
    claim_support_rate,
    mean_reciprocal_rank,
    precision_at_k,
    recall_at_k,
    token_f1,
)


def main() -> None:
    relevance = [1, 0, 1, 0, 0]
    query_relevance = [
        [1, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
    ]

    print("Retrieval evaluation")
    print("Precision@3:", round(precision_at_k(relevance, 3), 3))
    print("Recall@3:", round(recall_at_k(relevance, total_relevant=3, k=3), 3))
    print("Average precision:", round(average_precision(relevance, total_relevant=3), 3))
    print("Mean reciprocal rank:", round(mean_reciprocal_rank(query_relevance), 3))

    reference = "the system should abstain when evidence is insufficient"
    prediction = "the system should abstain if evidence is insufficient"
    print("\nAnswer evaluation")
    print("Token F1:", round(token_f1(reference, prediction), 3))
    print("Claim support rate:", round(claim_support_rate(4, 5), 3))
    print("Citation precision:", round(citation_precision(3, 4), 3))
    print(
        "Answerability accuracy:",
        round(
            answerability_accuracy(
                expected_answerable=[True, True, False, False],
                answered=[True, True, False, True],
            ),
            3,
        ),
    )


if __name__ == "__main__":
    main()
