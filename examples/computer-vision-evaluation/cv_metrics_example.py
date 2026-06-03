"""Worked example for computer vision evaluation metrics.

Run from the repository root:

    python examples/computer-vision-evaluation/cv_metrics_example.py

The example uses synthetic data only. It demonstrates the evaluation logic for
image classification, segmentation, and object detection without relying on any
private or domain-specific dataset.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.computer_vision_metrics import (  # noqa: E402
    Detection,
    GroundTruthBox,
    binary_dice,
    binary_iou,
    box_iou,
    classification_confusion_matrix,
    detection_summary,
    multiclass_iou,
    per_class_precision_recall_f1,
    pixel_accuracy,
)


def print_section(title: str) -> None:
    """Print a clean section title."""
    print("\n" + "=" * len(title))
    print(title)
    print("=" * len(title))


def classification_demo() -> None:
    """Evaluate a synthetic image classification model."""
    print_section("Image classification evaluation")

    y_true = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2]
    y_pred = [0, 0, 1, 1, 1, 0, 2, 2, 1, 2]
    labels = [0, 1, 2]
    label_names = {0: "background", 1: "object_a", 2: "object_b"}

    confusion = classification_confusion_matrix(y_true, y_pred, labels=labels)
    report = per_class_precision_recall_f1(confusion)

    print("Confusion matrix rows=true, columns=predicted")
    print(confusion)
    print("\nPer-class metrics")
    for index, label in enumerate(labels):
        print(
            f"- {label_names[label]}: "
            f"precision={report['precision'][index]:.3f}, "
            f"recall={report['recall'][index]:.3f}, "
            f"f1={report['f1'][index]:.3f}, "
            f"support={report['support'][index]}"
        )
    print(f"Macro F1: {report['macro_f1']:.3f}")


def segmentation_demo() -> None:
    """Evaluate synthetic binary and multiclass segmentation masks."""
    print_section("Segmentation evaluation")

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

    print(f"Binary IoU: {binary_iou(binary_true, binary_pred):.3f}")
    print(f"Binary Dice: {binary_dice(binary_true, binary_pred):.3f}")
    print(f"Pixel accuracy: {pixel_accuracy(binary_true, binary_pred):.3f}")

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

    print("\nMulticlass IoU")
    for label, score in multiclass_iou(multiclass_true, multiclass_pred).items():
        print(f"- class {label}: {score:.3f}")


def detection_demo() -> None:
    """Evaluate synthetic object detection predictions."""
    print_section("Object detection evaluation")

    ground_truth = [
        GroundTruthBox(image_id="img_001", label="widget", box=(10, 10, 50, 50)),
        GroundTruthBox(image_id="img_001", label="widget", box=(60, 60, 100, 100)),
        GroundTruthBox(image_id="img_002", label="widget", box=(15, 20, 55, 70)),
    ]
    predictions = [
        Detection(image_id="img_001", label="widget", score=0.95, box=(12, 12, 48, 48)),
        Detection(image_id="img_001", label="widget", score=0.80, box=(58, 58, 99, 101)),
        Detection(image_id="img_002", label="widget", score=0.60, box=(80, 80, 120, 120)),
        Detection(image_id="img_002", label="widget", score=0.55, box=(16, 21, 54, 69)),
    ]

    print("Example IoU between first prediction and first ground truth:")
    print(f"IoU = {box_iou(predictions[0].box, ground_truth[0].box):.3f}")

    summary = detection_summary(predictions, ground_truth, iou_threshold=0.5, label="widget")
    print("\nDetection summary at IoU threshold 0.5")
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"- {key}: {value:.3f}")
        else:
            print(f"- {key}: {value}")


if __name__ == "__main__":
    classification_demo()
    segmentation_demo()
    detection_demo()
