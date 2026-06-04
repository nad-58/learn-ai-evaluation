# 012 — Medical AI Evaluation

This tutorial introduces technical evaluation methods for AI systems used in medical or health-related contexts. The focus is model and system evaluation, not clinical validation, clinical claims, regulatory approval, or deployment advice.

Medical AI evaluation needs more care than a generic machine learning benchmark because the same headline metric can hide important behaviour. A model can have high overall accuracy while missing rare positive cases, performing poorly on images from a specific acquisition source, or producing poorly calibrated risk scores. For this reason, medical AI evaluation should normally consider task definition, dataset representativeness, threshold selection, subgroup performance, calibration, robustness, failure cases, and lifecycle monitoring.

## Learning objectives

After completing this tutorial, you should be able to:

1. Explain why accuracy alone is usually insufficient for medical AI evaluation.
2. Calculate sensitivity, specificity, precision, negative predictive value, F1 score, balanced accuracy, false positive rate, and false negative rate.
3. Compare decision thresholds using a threshold sweep.
4. Select a threshold against a pre-defined technical target, such as minimum sensitivity.
5. Review probability calibration using calibration bins and expected calibration error.
6. Compare performance across subgroups such as acquisition site, scanner type, image quality band, protocol, age band, or other justified groupings.
7. Prepare a public-safe evaluation report without confidential or client-specific information.

## Scope

This chapter is suitable for educational examples involving:

- binary classification, such as detecting whether a target finding is present or absent;
- risk scoring, where a model produces a probability-like output;
- image segmentation, where a predicted region is compared with a reference region;
- subgroup analysis, where performance is compared across meaningful data groups;
- technical evaluation reporting.

This chapter does not provide clinical validation guidance. It does not define medical claims, clinical safety requirements, or regulatory submission requirements. Any real health-related project should involve appropriately qualified clinical, technical, quality, privacy, and governance expertise.

## Why medical AI metrics need careful interpretation

In a balanced toy dataset, accuracy may look useful. In many medical datasets, however, the target condition may be rare. A model can achieve high accuracy by predicting the majority class too often. This can hide false negatives for positive cases or false positives that create unnecessary follow-up.

For binary tasks, the following metrics are commonly useful:

- **Sensitivity / recall**: among positive cases, how many did the model detect?
- **Specificity**: among negative cases, how many did the model correctly reject?
- **Precision / positive predictive value**: among predicted positives, how many were truly positive?
- **Negative predictive value**: among predicted negatives, how many were truly negative?
- **Balanced accuracy**: the average of sensitivity and specificity.
- **False positive rate**: the proportion of negative cases incorrectly marked positive.
- **False negative rate**: the proportion of positive cases incorrectly marked negative.

The best metric depends on the intended use, the risk of different error types, the role of the human user, and the expected operating environment. For education, always define the task and decision threshold before interpreting performance.

## Threshold selection

Many medical AI models output a score between 0 and 1. The threshold converts this score into a binary decision. Changing the threshold changes the trade-off between sensitivity and specificity.

A public-safe threshold analysis should document:

1. the candidate thresholds tested;
2. the metric target used to select the threshold;
3. whether the threshold was selected before or after looking at the test set;
4. whether the threshold is fixed after evaluation;
5. how threshold behaviour differs across subgroups.

The example in this phase shows how to sweep thresholds and select a threshold that meets a minimum sensitivity target. This is only a technical demonstration. In a real project, the threshold rationale must be justified and documented before final testing.

## Calibration

Calibration asks whether predicted probabilities match observed outcome frequencies. For example, among samples scored around 0.8, approximately 80% should be positive if the model is well calibrated. Calibration is important when model outputs are interpreted as risk scores or probabilities.

A simple calibration review can include:

- binning predictions into probability ranges;
- comparing the mean predicted score with the observed event rate in each bin;
- calculating an expected calibration error;
- reviewing whether calibration differs across relevant subgroups.

Calibration does not replace discrimination metrics. A model can rank cases well but be poorly calibrated, or be calibrated on average while still performing poorly for important subgroups.

## Subgroup performance

Overall performance can hide uneven behaviour. Subgroup analysis helps identify whether performance changes across data groups. Example groupings may include acquisition site, device type, scanner type, protocol, image quality band, demographic grouping, or disease severity band.

Subgroup analysis should be planned carefully. Small groups can produce unstable estimates, and sensitive attributes require appropriate privacy and governance controls. When reporting subgroup results, include group sizes and avoid over-interpreting very small sample counts.

## Segmentation volume comparison

For segmentation tasks, overlap metrics such as Dice and IoU are useful, but they may not fully describe clinically relevant measurement differences. A model may have a good overlap score while still over-estimating or under-estimating a region volume. This phase therefore includes a simple volume-difference utility for binary masks.

The segmentation example reports:

- reference volume;
- predicted volume;
- absolute volume difference;
- relative volume difference.

This is intentionally simple and should be extended for real projects with task-specific measurement definitions and review processes.

## Recommended workflow

A practical technical evaluation workflow is:

1. Define the intended technical task.
2. Define the evaluation dataset and inclusion/exclusion rules.
3. Check dataset quality, leakage risk, class balance, and subgroup coverage.
4. Lock the evaluation protocol before final testing.
5. Evaluate discrimination metrics and threshold behaviour.
6. Evaluate calibration where probabilities are used.
7. Evaluate subgroup performance and robustness.
8. Review failure cases with domain expertise.
9. Document limitations clearly.
10. Define lifecycle monitoring triggers for future re-evaluation.

## Related files

```text
src/learn_ai_evaluation/medical_ai_evaluation.py
examples/medical-ai-evaluation/medical_ai_binary_example.py
templates/medical-ai-evaluation-report-template.md
```

## Public-safe note

All examples in this chapter use synthetic data. They are designed for learning metric logic and report structure. Do not use these examples to make clinical claims or deployment decisions.
