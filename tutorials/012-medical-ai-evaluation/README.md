# 012 — Medical AI Evaluation

This tutorial introduces technical evaluation methods for AI systems used in medical or health-related contexts. The focus is model and system evaluation, not clinical validation, clinical claims, regulatory approval, or deployment advice.

The chapter is written from the practical perspective of reviewing AI-enabled medical devices. In that setting, a headline metric is never enough. The reviewer needs to understand the complete evidence chain: how the data were collected and labelled, how the model was trained and tested, how the decision threshold was selected, how the model behaves after software integration, how changes are controlled, and how performance will be monitored over time.

Medical AI evaluation needs more care than a generic machine learning benchmark because the same overall result can hide important behaviour. A model may show high accuracy while missing rare positive cases, performing inconsistently across sites or devices, producing poorly calibrated scores, or failing after integration with preprocessing and post-processing components.

## Reviewer perspective

A practical review should ask whether the evidence is complete, traceable, reproducible, and relevant to the intended technical use. The review should not focus only on the final model report. It should connect the following parts of the AI lifecycle:

1. intended task and model output;
2. dataset origin, representativeness, quality, and independence;
3. labelling process and reference-standard quality;
4. training, validation, and test separation;
5. model-level performance and uncertainty;
6. subgroup, site, device, and protocol performance;
7. robustness and failure behaviour;
8. software integration and system-level testing;
9. model change, retraining, and re-evaluation controls;
10. post-deployment monitoring and drift triggers.

This approach reflects a core reviewer principle: good model performance does not automatically demonstrate good system performance.

## Learning objectives

After completing this tutorial, you should be able to:

1. Explain why accuracy alone is usually insufficient for medical AI evaluation.
2. Calculate sensitivity, specificity, precision, negative predictive value, F1 score, balanced accuracy, false positive rate, and false negative rate.
3. Compare decision thresholds using a threshold sweep.
4. Review probability calibration using calibration bins and expected calibration error.
5. Compare performance across meaningful groups such as site, scanner type, protocol, image quality band, or demographic grouping.
6. Identify evidence gaps involving data leakage, label quality, software integration, model updates, and monitoring.
7. Prepare a public-safe technical evaluation report without confidential or client-specific information.

## Scope

This chapter supports educational evaluation of binary classification, risk scoring, image segmentation, subgroup analysis, robustness, and technical evidence reporting.

It does not provide clinical validation guidance, define clinical claims, or establish whether a product is suitable for clinical use. Real health-related projects require appropriately qualified clinical, technical, quality, privacy, and governance expertise.

## 1. Define the intended technical task

The evaluation should begin with a precise statement of the model input, output, decision unit, user interaction, and technical purpose. Avoid broad statements such as “the model detects disease” when the actual function is narrower, for example producing a probability, highlighting a region, segmenting an anatomy, or prioritising an image for review.

The unit of prediction must also be clear. A model may produce one result per frame, image, lesion, examination, subject, case, or episode. The split strategy and reported metrics should match that unit.

## 2. Review the dataset before reviewing the model

A reviewer should determine whether the evaluation dataset is relevant to the intended environment and sufficiently independent from development data. Important checks include:

- subject-level separation across training, validation, and test sets;
- repeated scans, frames, patches, crops, and derived samples;
- duplicate and near-duplicate observations;
- site, device, scanner, protocol, and acquisition coverage;
- class balance and positive-case support;
- exclusion rules and missing data;
- whether preprocessing was fitted using training data only;
- whether test data influenced model or threshold selection.

Random image-level splitting is often inappropriate when several images belong to the same subject or examination because it can create leakage and overestimate generalisation.

## 3. Review ground-truth quality

Model performance is meaningful only relative to the quality of the reference labels. The reviewer should understand:

- who produced the labels;
- the annotation instructions and acceptance rules;
- the relevant competence of annotators;
- whether annotators were blinded to model output;
- how disagreements were handled;
- whether consensus, adjudication, or an external reference was used;
- whether label uncertainty was measured;
- whether the reference process was consistent across sites.

Weak or inconsistent labels can limit the interpretation of otherwise strong model metrics.

## 4. Review model performance beyond accuracy

For binary tasks, useful metrics include sensitivity, specificity, precision, negative predictive value, balanced accuracy, false positive rate, and false negative rate.

A reviewer should check whether:

- the selected metrics match the intended technical task;
- denominators and case counts are reported;
- confidence intervals or other uncertainty measures are included;
- the operating threshold is predefined and justified;
- the final test set was used only after the model and threshold were fixed;
- failed or unavailable model outputs are counted rather than silently removed.

A point estimate without sample support can be misleading. Perfect sensitivity based on a few positive cases provides weak evidence.

## 5. Review thresholds and calibration

Changing a decision threshold changes the balance between false positives and false negatives. The threshold should be selected using development or validation data and then fixed before final testing.

When scores are interpreted as probabilities or risks, calibration should also be reviewed. A model may rank cases well while producing poorly calibrated probability values. Calibration should be assessed overall and, where justified, across sites or other relevant groups.

## 6. Review subgroup and multi-site performance

Overall performance can hide important differences. Evaluate performance across meaningful groups such as:

- acquisition site;
- scanner or device family;
- protocol or software version;
- image quality band;
- age or other justified demographic grouping;
- disease severity or object size;
- internal versus external data source.

Group results should include sample size, positive-case count, uncertainty, and limitations. Small groups should not be over-interpreted. A reviewer should also check whether an acceptable performance gap or investigation trigger has been defined.

## 7. Review robustness and failure behaviour

Robustness testing should reflect realistic sources of variation rather than only artificial noise. Relevant tests may include lower image quality, acquisition differences, incomplete metadata, borderline cases, rare presentations, preprocessing changes, and out-of-distribution inputs.

Failure review should classify false positives, false negatives, segmentation failures, unavailable outputs, and systematic group-specific errors. The purpose is not only to count failures but to understand their causes, detect recurring patterns, and define mitigation.

## 8. Review system-level performance

An AI-enabled medical device may contain several models plus preprocessing, post-processing, rules, user-interface logic, and software dependencies. Individual model performance does not automatically describe the performance of the complete system.

The review should consider:

- interactions between multiple models;
- cumulative or conditional decision logic;
- preprocessing and post-processing effects;
- handling of missing or invalid inputs;
- software and hardware dependencies;
- latency, resource limits, and failed inference;
- user-interface presentation and human review;
- consistency between model-level and system-level claims.

Where several models contribute to one output, the combined system behaviour should be evaluated rather than relying only on separate component metrics.

## 9. Review model change and retraining controls

Any change that can affect behaviour should trigger an impact assessment. Examples include changes to training data, labels, architecture, preprocessing, threshold, inference framework, post-processing, or input specification.

The reviewer should expect clear evidence of:

- what changed and why;
- whether the model remains fixed after release;
- which previous evidence may be affected;
- regression testing and acceptance criteria;
- re-evaluation of overall and group performance;
- version control for model, data, code, and configuration;
- criteria for deciding whether a wider review is required.

Uncontrolled or continuous model adaptation requires a different level of lifecycle control from a fixed released model.

## 10. Review monitoring and re-evaluation

Monitoring should be linked to predefined actions. Useful signals may include input drift, prediction drift, calibration change, error reports, subgroup performance, acquisition-source changes, and software or model updates.

A monitoring plan should define:

- what is monitored;
- data quality and minimum sample requirements;
- review frequency;
- quantitative or qualitative triggers;
- who investigates a trigger;
- what mitigation or re-evaluation follows;
- how monitoring evidence is recorded.

Monitoring without thresholds, ownership, and action criteria is incomplete.

## Recommended review workflow

1. Define the intended technical task and evaluation unit.
2. Trace the dataset from collection through final test selection.
3. Assess label quality, independence, leakage, and representativeness.
4. Review model metrics, uncertainty, calibration, and thresholds.
5. Compare performance across meaningful groups and environments.
6. Examine robustness, failure cases, and unavailable outputs.
7. Verify integrated system-level behaviour.
8. Assess change management, retraining, and regression testing.
9. Confirm monitoring triggers, responsibilities, and re-evaluation actions.
10. Document evidence gaps and limitations without over-claiming.

## Related files

```text
src/learn_ai_evaluation/medical_ai_evaluation.py
src/learn_ai_evaluation/medical_ai_metrics.py
examples/medical-ai-evaluation/medical_ai_binary_example.py
examples/medical-ai-evaluation/medical_ai_evaluation_example.py
templates/medical-ai-evaluation-report-template.md
```

## Public-safe note

All examples use synthetic or generalised data. The chapter does not include client names, device-specific findings, confidential assessment material, internal procedures, or identifiable patient information.