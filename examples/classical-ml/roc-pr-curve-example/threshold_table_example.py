"""Example: threshold table for ROC and precision-recall analysis."""

from learn_ai_evaluation.threshold_metrics import evaluate_thresholds


def main():
    y_true = [1, 1, 0, 1, 1, 0, 0, 0, 1, 0]
    scores = [0.90, 0.80, 0.70, 0.60, 0.55, 0.54, 0.53, 0.51, 0.50, 0.40]
    thresholds = [0.80, 0.70, 0.60, 0.53, 0.50, 0.30]

    results = evaluate_thresholds(y_true, scores, thresholds)

    header = "threshold,tp,fp,tn,fn,tpr,fpr,precision,recall"
    print(header)
    for row in results:
        print(
            f"{row.threshold:.2f},{row.tp},{row.fp},{row.tn},{row.fn},"
            f"{row.tpr:.4f},{row.fpr:.4f},{row.precision:.4f},{row.recall:.4f}"
        )


if __name__ == "__main__":
    main()
