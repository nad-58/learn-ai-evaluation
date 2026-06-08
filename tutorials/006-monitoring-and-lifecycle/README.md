# Phase 6: Monitoring and Lifecycle Evaluation

This tutorial covers post-validation evaluation of AI systems. A system may perform well during testing but change over time because the input data, workflow, users, environment, labels, or software version changes.

## Aim

Monitoring and lifecycle evaluation checks whether the current system behaviour remains consistent with the reference baseline. It supports routine review, early warning, investigation, mitigation, and re-evaluation.

## Main questions

1. What was the reference baseline?
2. What is the current monitoring window?
3. Are performance metrics still acceptable?
4. Has the input data distribution changed?
5. Have warning or action thresholds been crossed?
6. Is routine monitoring enough, or is further review required?

## Key terms

**Reference window:** the baseline period or dataset used to define expected system behaviour.

**Current window:** the new data period being reviewed.

**Drift:** a measurable change between the reference data and current data.

**Threshold rule:** a predefined warning or action level for a metric.

**Lifecycle decision:** a documented decision such as routine monitoring, increased monitoring, data shift review, or re-evaluation.

## Utilities

The code for this phase is in:

```text
src/learn_ai_evaluation/monitoring_lifecycle.py
```

It includes utilities for binary classification metrics, Population Stability Index, feature drift reporting, threshold checks, and lifecycle decision summaries.

## Worked example

Run from the repository root:

```bash
python examples/monitoring-and-lifecycle/monitoring_lifecycle_example.py
```

The example trains a simple model, creates a reference monitoring window, simulates a changed current window, calculates current performance, checks thresholds, reviews feature drift, and prints a lifecycle decision.

## Suggested report content

A monitoring report should record the system version, data version, reference baseline, current monitoring period, metrics, thresholds, drift results, warning flags, investigation notes, decision, owner, and next review date.

## Practical interpretation

A drift flag is not a final conclusion. It is a signal that the data or operating context may have changed. The result should be reviewed together with performance metrics, known limitations, evidence quality, and the intended use of the system.
