"""Numerical image-segmentation evaluation example.

Run from the repository root:

    python examples/computer-vision-evaluation/segmentation_metrics_example.py
"""
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.computer_vision_metrics import (
    binary_dice,
    binary_iou,
    multiclass_iou,
    pixel_accuracy,
)


def main() -> None:
    binary_true = np.array(
        [
            [0, 0, 1, 1],
            [0, 1, 1, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 0],
        ]
    )
    binary_pred = np.array(
        [
            [0, 0, 1, 0],
            [0, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
    )

    print("BINARY SEGMENTATION")
    print("Ground truth mask:\n", binary_true)
    print("Prediction mask:\n", binary_pred)
    print(f"Pixel accuracy: {pixel_accuracy(binary_true, binary_pred):.3f}")
    print(f"IoU:            {binary_iou(binary_true, binary_pred):.3f}")
    print(f"Dice:           {binary_dice(binary_true, binary_pred):.3f}")

    multiclass_true = np.array(
        [
            [0, 0, 1, 1],
            [0, 2, 2, 1],
            [0, 2, 2, 1],
            [0, 0, 0, 0],
        ]
    )
    multiclass_pred = np.array(
        [
            [0, 0, 1, 1],
            [0, 2, 1, 1],
            [0, 2, 2, 0],
            [0, 0, 0, 0],
        ]
    )

    print("\nMULTICLASS SEGMENTATION")
    for label, score in multiclass_iou(multiclass_true, multiclass_pred).items():
        print(f"class {label}: IoU={score:.3f}")


if __name__ == "__main__":
    main()
