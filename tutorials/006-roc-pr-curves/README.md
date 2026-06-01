# 006 — ROC and Precision-Recall Curves

## Purpose

This tutorial explains how to evaluate a binary classifier when the model outputs a probability score rather than only a class label.

A probability score can be converted into a class label using a threshold. By changing the threshold, we can study how the model behaves under different decision settings.

## Example data

We use a small example with 10 samples.

| Sample | True label | Score |
|---:|---:|---:|
| 1 | 1 | 0.90 |
| 2 | 1 | 0.80 |
| 3 | 0 | 0.70 |
| 4 | 1 | 0.60 |
| 5 | 1 | 0.55 |
| 6 | 0 | 0.54 |
| 7 | 0 | 0.53 |
| 8 | 0 | 0.51 |
| 9 | 1 | 0.50 |
| 10 | 0 | 0.40 |

We evaluate the model at these thresholds:

```text
0.80, 0.70, 0.60, 0.53, 0.50, 0.30
```

## ROC curve

The ROC curve compares:

```text
TPR = TP / (TP + FN)
FPR = FP / (FP + TN)
```

Each threshold gives one point on the ROC curve.

## Precision-recall curve

The precision-recall curve compares:

```text
Precision = TP / (TP + FP)
Recall = TP / (TP + FN)
```

Precision-recall curves are often useful when the positive class is relatively rare or when positive-case detection is the main focus.

## Why this matters

A default threshold, such as 0.50, is not always the best choice. Threshold analysis helps show the trade-off between different metrics.

## Key takeaway

ROC and precision-recall curves help evaluate a classifier across multiple thresholds instead of relying on a single threshold.
