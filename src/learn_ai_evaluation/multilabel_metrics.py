"""Simple multi-label metric utilities."""

from __future__ import annotations


def exact_match_ratio(y_true: list[set], y_pred: list[set]) -> float:
    if not y_true:
        return 0.0
    matches = sum(1 for true_labels, pred_labels in zip(y_true, y_pred) if true_labels == pred_labels)
    return matches / len(y_true)


def jaccard_index(true_labels: set, pred_labels: set) -> float:
    union = true_labels | pred_labels
    if not union:
        return 1.0
    intersection = true_labels & pred_labels
    return len(intersection) / len(union)


def average_jaccard_index(y_true: list[set], y_pred: list[set]) -> float:
    if not y_true:
        return 0.0
    values = [jaccard_index(t, p) for t, p in zip(y_true, y_pred)]
    return sum(values) / len(values)


def hamming_loss_sets(y_true: list[set], y_pred: list[set], all_labels: set) -> float:
    if not y_true or not all_labels:
        return 0.0

    errors = 0
    total = len(y_true) * len(all_labels)

    for true_labels, pred_labels in zip(y_true, y_pred):
        for label in all_labels:
            true_has_label = label in true_labels
            pred_has_label = label in pred_labels
            if true_has_label != pred_has_label:
                errors += 1

    return errors / total
