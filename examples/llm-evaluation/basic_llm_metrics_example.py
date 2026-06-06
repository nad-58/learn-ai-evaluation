"""Worked example for foundational LLM evaluation metrics.

Run from the repository root:

    python examples/llm-evaluation/basic_llm_metrics_example.py
"""

from pathlib import Path
from pprint import pprint
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.llm_metrics import (  # noqa: E402
    bleu_1,
    exact_match,
    perplexity,
    rouge_l_f1,
    rouge_n_recall,
    token_f1,
)


def main() -> None:
    reference = "the model returns a concise and correct answer"
    prediction = "the model gives a correct concise answer"

    print("Reference:", reference)
    print("Prediction:", prediction)
    print()

    print("Exact match:", exact_match(prediction, reference))
    print("Token precision, recall and F1:")
    pprint(token_f1(prediction, reference))
    print("ROUGE-1 recall:", round(rouge_n_recall(prediction, reference, n=1), 3))
    print("ROUGE-2 recall:", round(rouge_n_recall(prediction, reference, n=2), 3))
    print("ROUGE-L F1:", round(rouge_l_f1(prediction, reference), 3))
    print("BLEU-1:", round(bleu_1(prediction, reference), 3))

    probabilities = [0.70, 0.55, 0.82, 0.61, 0.77]
    print("Perplexity:", round(perplexity(probabilities), 3))

    print("\nInterpretation")
    print("- Exact match can fail even when the meaning is similar.")
    print("- Token and n-gram metrics reward lexical overlap.")
    print("- Perplexity measures token prediction, not answer correctness.")
    print("- Add semantic, judge-based and human evaluation for open-ended tasks.")


if __name__ == "__main__":
    main()
