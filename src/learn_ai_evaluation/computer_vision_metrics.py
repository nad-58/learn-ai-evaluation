"""Computer vision evaluation utilities for Learn AI Evaluation.

The functions in this module are intentionally lightweight and public-safe.
They use small NumPy examples so learners can understand the metric logic
before adopting larger libraries or production evaluation pipelines.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Sequence

import numpy as np


ArrayLike = Sequence[float] | np.ndarray


def _as_numpy(values: ArrayLike) -> np.ndarray:
    """Convert values to a NumPy array without changing numeric content."""
    return np.asarray(values)


def safe_divide(numerator: float, denominator: float) -> float:
    """Divide safely and return 0.0 when the denominator is zero."""
    if denominator == 0:
        return 0.0
    return float(numerator / denominator)


def classification_confusion_matrix(
    y_true: Sequence[int],
    y_pred: Sequence[int],
    labels: Optional[Sequence[int]] = None,
) -> np.ndarray:
    """Return a confusion matrix for image classification.

    Rows represent ground-truth classes and columns represent predicted classes.
    """
    true = _as_numpy(y_true).astype(int)
    pred = _as_numpy(y_pred).astype(int)
    if true.shape[0] != pred.shape[0]:
        raise ValueError("y_true and y_pred must contain the same number of items")

    if labels is None:
        labels = sorted(set(true.tolist()) | set(pred.tolist()))
    label_to_index = {label: index for index, label in enumerate(labels)}

    matrix = np.zeros((len(labels), len(labels)), dtype=int)
    for target, output in zip(true, pred):
        if target in label_to_index and output in label_to_index:
            matrix[label_to_index[target], label_to_index[output]] += 1
    return matrix


def per_class_precision_recall_f1(confusion_matrix: np.ndarray) -> dict[str, np.ndarray]:
    """Calculate per-class precision, recall, and F1 from a confusion matrix."""
    cm = _as_numpy(confusion_matrix).astype(float)
    true_positive = np.diag(cm)
    false_positive = cm.sum(axis=0) - true_positive
    false_negative = cm.sum(axis=1) - true_positive

    precision = np.array([
        safe_divide(tp, tp + fp) for tp, fp in zip(true_positive, false_positive)
    ])
    recall = np.array([
        safe_divide(tp, tp + fn) for tp, fn in zip(true_positive, false_negative)
    ])
    f1 = np.array([
        safe_divide(2 * p * r, p + r) for p, r in zip(precision, recall)
    ])
    support = cm.sum(axis=1).astype(int)

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "support": support,
        "macro_precision": float(np.mean(precision)) if precision.size else 0.0,
        "macro_recall": float(np.mean(recall)) if recall.size else 0.0,
        "macro_f1": float(np.mean(f1)) if f1.size else 0.0,
    }


def pixel_accuracy(mask_true: np.ndarray, mask_pred: np.ndarray, ignore_label: Optional[int] = None) -> float:
    """Return pixel accuracy for segmentation masks."""
    true = _as_numpy(mask_true)
    pred = _as_numpy(mask_pred)
    if true.shape != pred.shape:
        raise ValueError("mask_true and mask_pred must have the same shape")

    valid = np.ones(true.shape, dtype=bool)
    if ignore_label is not None:
        valid = true != ignore_label
    return safe_divide(float(np.sum((true == pred) & valid)), float(np.sum(valid)))


def binary_iou(mask_true: np.ndarray, mask_pred: np.ndarray) -> float:
    """Return Intersection over Union for binary segmentation masks."""
    true = _as_numpy(mask_true).astype(bool)
    pred = _as_numpy(mask_pred).astype(bool)
    if true.shape != pred.shape:
        raise ValueError("mask_true and mask_pred must have the same shape")

    intersection = np.logical_and(true, pred).sum()
    union = np.logical_or(true, pred).sum()
    return safe_divide(float(intersection), float(union))


def binary_dice(mask_true: np.ndarray, mask_pred: np.ndarray) -> float:
    """Return Dice score for binary segmentation masks."""
    true = _as_numpy(mask_true).astype(bool)
    pred = _as_numpy(mask_pred).astype(bool)
    if true.shape != pred.shape:
        raise ValueError("mask_true and mask_pred must have the same shape")

    intersection = np.logical_and(true, pred).sum()
    total_positive = true.sum() + pred.sum()
    return safe_divide(float(2 * intersection), float(total_positive))


def multiclass_iou(
    mask_true: np.ndarray,
    mask_pred: np.ndarray,
    labels: Optional[Iterable[int]] = None,
    ignore_label: Optional[int] = None,
) -> dict[int, float]:
    """Return per-class IoU for multi-class segmentation."""
    true = _as_numpy(mask_true)
    pred = _as_numpy(mask_pred)
    if true.shape != pred.shape:
        raise ValueError("mask_true and mask_pred must have the same shape")

    if labels is None:
        labels = sorted(set(true.flatten().tolist()) | set(pred.flatten().tolist()))

    scores: dict[int, float] = {}
    for label in labels:
        if ignore_label is not None and label == ignore_label:
            continue
        true_label = true == label
        pred_label = pred == label
        intersection = np.logical_and(true_label, pred_label).sum()
        union = np.logical_or(true_label, pred_label).sum()
        scores[int(label)] = safe_divide(float(intersection), float(union))
    return scores


def box_iou(box_a: ArrayLike, box_b: ArrayLike) -> float:
    """Return IoU for two bounding boxes in [x_min, y_min, x_max, y_max] format."""
    a = _as_numpy(box_a).astype(float)
    b = _as_numpy(box_b).astype(float)
    if a.shape[0] != 4 or b.shape[0] != 4:
        raise ValueError("Each box must contain four values: x_min, y_min, x_max, y_max")

    x_left = max(a[0], b[0])
    y_top = max(a[1], b[1])
    x_right = min(a[2], b[2])
    y_bottom = min(a[3], b[3])

    intersection_width = max(0.0, x_right - x_left)
    intersection_height = max(0.0, y_bottom - y_top)
    intersection = intersection_width * intersection_height

    area_a = max(0.0, a[2] - a[0]) * max(0.0, a[3] - a[1])
    area_b = max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])
    union = area_a + area_b - intersection
    return safe_divide(intersection, union)


@dataclass(frozen=True)
class Detection:
    """Simple detection record used by the educational detection evaluator."""

    image_id: str
    label: str
    score: float
    box: tuple[float, float, float, float]


@dataclass(frozen=True)
class GroundTruthBox:
    """Simple ground-truth bounding box record."""

    image_id: str
    label: str
    box: tuple[float, float, float, float]


def precision_recall_for_detections(
    predictions: Sequence[Detection],
    ground_truth: Sequence[GroundTruthBox],
    iou_threshold: float = 0.5,
    label: Optional[str] = None,
) -> dict[str, np.ndarray | float | int]:
    """Calculate detection precision and recall arrays for one class or all classes.

    A prediction is counted as a true positive only when it matches an unused
    ground-truth box from the same image and class at or above the IoU threshold.
    """
    if label is not None:
        predictions = [item for item in predictions if item.label == label]
        ground_truth = [item for item in ground_truth if item.label == label]

    sorted_predictions = sorted(predictions, key=lambda item: item.score, reverse=True)
    matched_gt: set[int] = set()
    true_positives = []
    false_positives = []

    for prediction in sorted_predictions:
        candidate_indices = [
            index
            for index, gt in enumerate(ground_truth)
            if gt.image_id == prediction.image_id and gt.label == prediction.label and index not in matched_gt
        ]
        candidate_ious = [box_iou(prediction.box, ground_truth[index].box) for index in candidate_indices]

        if candidate_ious and max(candidate_ious) >= iou_threshold:
            best_local_index = int(np.argmax(candidate_ious))
            matched_gt.add(candidate_indices[best_local_index])
            true_positives.append(1)
            false_positives.append(0)
        else:
            true_positives.append(0)
            false_positives.append(1)

    cumulative_tp = np.cumsum(true_positives)
    cumulative_fp = np.cumsum(false_positives)
    precision = np.array([
        safe_divide(tp, tp + fp) for tp, fp in zip(cumulative_tp, cumulative_fp)
    ])
    recall = np.array([
        safe_divide(tp, len(ground_truth)) for tp in cumulative_tp
    ])

    return {
        "precision": precision,
        "recall": recall,
        "true_positive_count": int(cumulative_tp[-1]) if cumulative_tp.size else 0,
        "false_positive_count": int(cumulative_fp[-1]) if cumulative_fp.size else 0,
        "ground_truth_count": int(len(ground_truth)),
    }


def average_precision(precision: ArrayLike, recall: ArrayLike) -> float:
    """Calculate interpolated average precision from precision and recall arrays."""
    p = _as_numpy(precision).astype(float)
    r = _as_numpy(recall).astype(float)
    if p.shape != r.shape:
        raise ValueError("precision and recall must have the same shape")
    if p.size == 0:
        return 0.0

    order = np.argsort(r)
    r = r[order]
    p = p[order]

    recall_points = np.concatenate(([0.0], r, [1.0]))
    precision_points = np.concatenate(([0.0], p, [0.0]))

    for index in range(precision_points.size - 2, -1, -1):
        precision_points[index] = max(precision_points[index], precision_points[index + 1])

    changing_points = np.where(recall_points[1:] != recall_points[:-1])[0]
    return float(np.sum(
        (recall_points[changing_points + 1] - recall_points[changing_points])
        * precision_points[changing_points + 1]
    ))


def detection_summary(
    predictions: Sequence[Detection],
    ground_truth: Sequence[GroundTruthBox],
    iou_threshold: float = 0.5,
    label: Optional[str] = None,
) -> dict[str, float | int]:
    """Return a compact precision, recall, and AP summary for detections."""
    curve = precision_recall_for_detections(
        predictions=predictions,
        ground_truth=ground_truth,
        iou_threshold=iou_threshold,
        label=label,
    )
    precision = curve["precision"]
    recall = curve["recall"]
    return {
        "ground_truth_count": int(curve["ground_truth_count"]),
        "true_positive_count": int(curve["true_positive_count"]),
        "false_positive_count": int(curve["false_positive_count"]),
        "final_precision": float(precision[-1]) if len(precision) else 0.0,
        "final_recall": float(recall[-1]) if len(recall) else 0.0,
        "average_precision": average_precision(precision, recall),
        "iou_threshold": float(iou_threshold),
    }
