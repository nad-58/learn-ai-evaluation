# 004 — Robustness Evaluation

## Purpose

This chapter explains how to evaluate whether a model keeps acceptable performance when the input conditions change.

A model can perform well on a clean test set but degrade when the input data is noisy, lower quality, shifted, incomplete, or collected under different conditions.

## What robustness means

Robustness means that the model maintains useful performance under realistic input variation.

Examples of input variation include:

- image blur;
- image brightness change;
- lower resolution;
- missing feature values;
- sensor variation;
- text spelling variation;
- different data source;
- rare or unusual inputs.

## Practical workflow

```text
1. Define the robustness goal.
2. Choose the metric to measure.
3. Define the baseline dataset.
4. Define the changed-input dataset.
5. Set an acceptable performance drop.
6. Run the model on both datasets.
7. Compare the results.
8. Decide whether the robustness goal is met.
9. Investigate failure cases.
```

## Example — Accuracy drop

Suppose an image classifier has this baseline result:

```text
Baseline accuracy = 0.95
```

We decide that a drop of up to 0.05 is acceptable. Therefore, the robustness threshold is:

```text
Minimum acceptable accuracy = 0.95 - 0.05 = 0.90
```

Scenario 1:

```text
Accuracy on changed-input dataset = 0.91
Decision = pass
```

Scenario 2:

```text
Accuracy on changed-input dataset = 0.80
Decision = investigate
```

## What to investigate

If performance drops too much, check:

- whether the changed-input dataset is realistic;
- whether labels are correct;
- whether data quality is too low;
- whether the model has seen enough variation during training;
- whether preprocessing is consistent;
- whether one subgroup or condition is affected more than others.

## Key takeaway

Robustness evaluation should be planned. It is not enough to report one clean-test metric. The model should also be tested under realistic input changes.
