"""Numerical object-detection evaluation example.

Run from the repository root:

    python examples/computer-vision-evaluation/detection_metrics_example.py
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.computer_vision_metrics import (
    Detection,
    GroundTruthBox,
    box_iou,
    detection_summary,
)


def main() -> None:
    ground_truth = [
        GroundTruthBox("img_001", "widget", (10, 10, 50, 50)),
        GroundTruthBox("img_001", "widget", (60, 60, 100, 100)),
        GroundTruthBox("img_002", "widget", (15, 20, 55, 70)),
    ]
    predictions = [
        Detection("img_001", "widget", 0.95, (12, 12, 48, 48)),
        Detection("img_001", "widget", 0.80, (58, 58, 99, 101)),
        Detection("img_002", "widget", 0.60, (80, 80, 120, 120)),
        Detection("img_002", "widget", 0.55, (16, 21, 54, 69)),
    ]

    first_iou = box_iou(predictions[0].box, ground_truth[0].box)
    print(f"First prediction/ground-truth IoU: {first_iou:.3f}")

    summary = detection_summary(
        predictions,
        ground_truth,
        iou_threshold=0.5,
        label="widget",
    )
    print("\nDETECTION SUMMARY")
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"{key}: {value:.3f}")
        else:
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
