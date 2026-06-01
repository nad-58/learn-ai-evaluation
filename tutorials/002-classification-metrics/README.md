# 002 — Classification Metrics

This tutorial introduces the main metrics used for classification model evaluation.

Classification is one of the most common machine learning tasks. The model receives an input and predicts one class label. Examples include spam detection, quality inspection, image classification, and risk scoring.

## Why metrics matter

A model should not be evaluated using only one number. Accuracy can be useful, but it can be misleading when the dataset is imbalanced or when different mistake types matter differently.

A good evaluation should explain:

- how many predictions were correct;
- which classes were confused;
- whether the selected metric fits the task;
- whether the selected threshold is suitable.

## Confusion matrix

For binary classification, predictions can be summarised using four counts:

| Count | Meaning |
|---|---|
| TP | Predicted positive and label was positive |
| TN | Predicted negative and label was negative |
| FP | Predicted positive and label was negative |
| FN | Predicted negative and label was positive |

## Accuracy

```text
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

Accuracy measures the proportion of correct predictions.

## Precision

```text
Precision = TP / (TP + FP)
```

Precision measures the quality of positive predictions.

## Recall

```text
Recall = TP / (TP + FN)
```

Recall measures how many positive cases were detected.

## F1-score

```text
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

F1-score combines precision and recall.

## Worked example

```text
TP = 80
TN = 900
FP = 20
FN = 100
```

```text
Accuracy  = (80 + 900) / (80 + 900 + 20 + 100) = 0.8909
Precision = 80 / (80 + 20) = 0.8000
Recall    = 80 / (80 + 100) = 0.4444
F1-score  = 0.5714
```

This example shows why accuracy alone is not enough. The accuracy looks high, but recall is much lower.

## Metric selection

| Situation | Useful metric |
|---|---|
| Balanced classes | Accuracy |
| Positive prediction quality matters | Precision |
| Positive case detection matters | Recall |
| Precision and recall both matter | F1-score |
| Imbalanced classes | Precision, recall, F1, PR-AUC |
| Threshold needs review | Confusion matrix, ROC curve, PR curve |

## Key takeaway

Classification evaluation should start with the confusion matrix and then use metrics that match the purpose of the model.
