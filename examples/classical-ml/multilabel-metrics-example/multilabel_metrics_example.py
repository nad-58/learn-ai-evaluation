"""Example: multi-label classification metrics."""

from learn_ai_evaluation.multilabel_metrics import (
    exact_match_ratio,
    average_jaccard_index,
    hamming_loss_sets,
)


def main():
    all_labels = {"a", "b", "c", "d"}

    y_true = [
        {"a", "b"},
        {"c"},
        {"a", "d"},
        {"b", "c"},
    ]

    y_pred = [
        {"a", "b"},
        {"c", "d"},
        {"a"},
        {"b"},
    ]

    print("Exact match ratio:", round(exact_match_ratio(y_true, y_pred), 4))
    print("Average Jaccard index:", round(average_jaccard_index(y_true, y_pred), 4))
    print("Hamming loss:", round(hamming_loss_sets(y_true, y_pred, all_labels), 4))


if __name__ == "__main__":
    main()
