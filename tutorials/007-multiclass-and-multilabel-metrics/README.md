# 007 — Multi-Class and Multi-Label Metrics

## Purpose

This tutorial explains how classification evaluation changes when there are more than two classes or when one sample can have more than one label.

## Multi-class classification

In multi-class classification, each sample belongs to exactly one class from three or more possible classes.

Examples:

- classify an image as car, bicycle, or motorcycle;
- classify a document into one topic;
- classify a product defect into one defect category.

## Averaging strategies

Many metrics can be calculated per class and then averaged.

### Macro average

Macro average calculates the metric for each class and then takes the unweighted average.

This treats every class equally, even if some classes have fewer samples.

### Weighted average

Weighted average calculates the metric for each class and weights it by the number of samples in that class.

This reflects the dataset distribution more strongly.

### Micro average

Micro average aggregates counts across all classes before calculating the metric.

This treats every sample equally.

## Multi-label classification

In multi-label classification, one sample can have multiple labels at the same time.

Examples:

- an image can contain person, car, and road;
- a document can belong to several topics;
- a product can have multiple defect tags.

## Useful multi-label metrics

### Exact match ratio

Exact match ratio checks whether the full predicted label set exactly matches the true label set.

### Hamming loss

Hamming loss measures the fraction of labels that are incorrectly predicted.

### Jaccard index

Jaccard index compares the overlap between predicted labels and true labels.

```text
Jaccard = intersection / union
```

## Key takeaway

Binary classification metrics are the foundation, but multi-class and multi-label tasks require careful averaging and label-set evaluation.
