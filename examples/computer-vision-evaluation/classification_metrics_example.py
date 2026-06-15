"""Numerical image-classification evaluation example.

Run from the repository root:

    python examples/computer-vision-evaluation/classification_metrics_example.py
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.computer_vision_metrics import (
    classification_confusion_matrix,
    per_class_precision_recall_f1,
)


def main() -> None:
    y_true = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2]
    y_pred = [0, 0, 1, 1, 1, 0, 2, 2, 1, 2]
    labels = [0, 1, 2]
    names = {0: "background", 1: "object_a", 2: "object_b"}

    confusion = classification_confusion_matrix(y_true, y_pred, labels)
    report = per_class_precision_recall_f1(confusion)

    print("CONFUSION MATRIX: rows=true, columns=predicted")
    print(confusion)
    print("\nPER-CLASS METRICS")
    for index, label in enumerate(labels):
        print(
            f"{names[label]}: "
            f"precision={report['precision'][index]:.3f}, "
            f"recall={report['recall'][index]:.3f}, "
            f"f1={report['f1'][index]:.3f}, "
            f"support={report['support'][index]}"
        )
    print(f"\nMacro precision: {report['macro_precision']:.3f}")
    print(f"Macro recall:    {report['macro_recall']:.3f}")
    print(f"Macro F1:        {report['macro_f1']:.3f}")


if __name__ == "__main__":
    main()
