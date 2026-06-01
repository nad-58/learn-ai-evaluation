# 005 — Confusion Matrix and Threshold Selection

## Purpose

This tutorial explains how a decision threshold changes the behaviour of a binary classification model.

Many classifiers output a probability or score. A threshold converts that score into a class label.

```text
if score >= threshold: predict positive
else: predict negative
```

## Why threshold selection matters

Changing the threshold changes the balance between precision and recall.

A lower threshold usually increases recall but may reduce precision. A higher threshold usually increases precision but may reduce recall.

## Simple workflow

```text
1. Train the model.
2. Predict probability scores on validation data.
3. Try several thresholds.
4. Calculate metrics at each threshold.
5. Select a threshold that fits the task.
6. Confirm performance on independent test data.
```

## Example thresholds

| Threshold | Precision | Recall | F1-score |
|---:|---:|---:|---:|
| 0.30 | 0.55 | 0.88 | 0.68 |
| 0.50 | 0.72 | 0.70 | 0.71 |
| 0.70 | 0.86 | 0.42 | 0.56 |

The best threshold depends on the goal. There is no universal threshold that is always best.

## Key takeaway

The threshold is part of the evaluation design. Do not only report default-threshold results without checking whether the threshold is suitable for the task.
