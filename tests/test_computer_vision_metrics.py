import numpy as np

from learn_ai_evaluation.computer_vision_metrics import (
    Detection,
    GroundTruthBox,
    average_precision,
    binary_dice,
    binary_iou,
    box_iou,
    classification_confusion_matrix,
    detection_summary,
    multiclass_iou,
    per_class_precision_recall_f1,
    pixel_accuracy,
)


def test_classification_metrics():
    y_true = [0, 0, 1, 1, 2, 2]
    y_pred = [0, 1, 1, 1, 2, 0]
    confusion = classification_confusion_matrix(y_true, y_pred, labels=[0, 1, 2])
    report = per_class_precision_recall_f1(confusion)
    assert confusion.tolist() == [[1, 1, 0], [0, 2, 0], [1, 0, 1]]
    assert report["support"].tolist() == [2, 2, 2]
    assert 0.0 <= report["macro_f1"] <= 1.0


def test_binary_segmentation_metrics():
    true = np.array([[1, 1], [0, 0]])
    pred = np.array([[1, 0], [1, 0]])
    assert pixel_accuracy(true, pred) == 0.5
    assert binary_iou(true, pred) == 1 / 3
    assert binary_dice(true, pred) == 0.5


def test_multiclass_iou():
    true = np.array([[0, 1], [2, 2]])
    pred = np.array([[0, 1], [1, 2]])
    scores = multiclass_iou(true, pred)
    assert scores[0] == 1.0
    assert scores[1] == 0.5
    assert scores[2] == 0.5


def test_box_iou():
    assert box_iou((0, 0, 10, 10), (0, 0, 10, 10)) == 1.0
    assert box_iou((0, 0, 10, 10), (10, 10, 20, 20)) == 0.0


def test_detection_summary_and_average_precision():
    ground_truth = [GroundTruthBox("img", "object", (0, 0, 10, 10))]
    predictions = [
        Detection("img", "object", 0.9, (0, 0, 10, 10)),
        Detection("img", "object", 0.5, (20, 20, 30, 30)),
    ]
    summary = detection_summary(predictions, ground_truth, iou_threshold=0.5)
    assert summary["true_positive_count"] == 1
    assert summary["false_positive_count"] == 1
    assert summary["final_recall"] == 1.0
    assert summary["average_precision"] == 1.0
    assert average_precision([1.0, 0.5], [1.0, 1.0]) == 1.0
