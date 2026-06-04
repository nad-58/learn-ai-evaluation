# 013 — Medical AI Testing Plan

This chapter explains how to plan technical testing for AI functions used in health-related software. It is educational and public-safe. It does not reproduce confidential material, draft documents, client documents, or official requirements.

A good evaluation starts before metrics are calculated. The team should define what is being tested, why it is being tested, which data will be used, which environment will be used, who is responsible, what evidence will be produced, and what will happen when the model or pipeline changes.

## Define the AI function under test

A health AI system may contain several AI functions. Each function should be evaluated with a clear boundary. The plan should describe the function being tested, its inputs, outputs, interfaces, assumptions, and known limitations.

Example functions include a classifier, segmentation model, detection model, risk scoring model, measurement model, post-processing module, or multi-model pipeline.

For each function, the plan should identify whether testing is performed at model level, AI component level, integrated system level, or monitoring level. A model can pass isolated evaluation but still fail after integration because of preprocessing, post-processing, user interface, thresholding, data routing, or runtime environment differences.

## Test objectives

Test objectives should be specific and measurable. A weak objective is: "show the model works." A better objective is: "estimate sensitivity and specificity of the locked binary classifier on an independent patient-level test set using a predefined threshold."

Good objectives define the task, dataset, independence unit, primary metrics, secondary metrics, decision criteria, lifecycle stage, and limitations.

## Test scope

The scope should explain what is included and excluded. This is important when a system contains several models, rules, preprocessing, post-processing, and human interaction.

A useful scope statement answers: which function is tested, which version is tested, which input and output types are included, which operating modes are included, which interfaces are in scope, and which scenarios are out of scope.

## Roles and responsibilities

Testing should not be treated as a single-person activity. A realistic evaluation may require model developers, data engineers, software engineers, domain experts, quality reviewers, usability specialists, security specialists, and independent reviewers.

The plan should identify who is responsible for test planning, data selection, label management, model execution, metric calculation, statistical analysis, failure-case review, approval of deviations, reporting, and record keeping.

Where possible, the person who develops the model should not be the only person who approves the final test result. Independence helps reduce confirmation bias.

## Test environment and tools

The test environment should be documented because changes in hardware, software, libraries, preprocessing, random seeds, or runtime settings can affect model output.

Document hardware, operating system, software versions, library versions, model version, preprocessing and post-processing versions, thresholds, data access controls, logging, random seeds, and known differences between test and deployment environments.

Tools used for testing should be controlled and repeatable. This includes scripts, notebooks, metric calculators, annotation tools, data extraction tools, and report-generation utilities.

## Test data

The plan should describe how test data is selected, prepared, labelled, separated from training data, and protected against leakage. Health AI evaluation should normally consider patient-level or subject-level independence rather than row-level random splitting.

Important questions include the independence unit, repeated samples, separation between training and testing, label independence, inclusion rules, exclusion rules, subgroup counts, and documented handling of outliers.

## Test methods

A complete plan may combine metric-based evaluation, threshold analysis, calibration analysis, subgroup analysis, robustness testing, black-box input-output testing, comparison against a reference method, explainability review, transparency review, failure-case review, and integration testing.

The method should match the task. For example, a binary classifier needs sensitivity and specificity; a segmentation model needs overlap and measurement error; a risk model needs calibration; a multi-model pipeline needs component-level and system-level evaluation.

## Deliverables

Typical deliverables include a test protocol, dataset summary, split and leakage report, metric report, threshold report, calibration report, subgroup report, robustness report, failure-case summary, test-deviation log, and final evaluation conclusion.

## Re-testing after change

Any change to the AI function or surrounding pipeline can affect performance. The team should perform a change-impact assessment and decide whether full re-testing or partial re-testing is justified.

Changes that often require careful review include retraining, new training data, threshold change, architecture change, preprocessing change, post-processing change, labelling change, reference change, software-library change, deployment-environment change, and user-interface change.

## Related files

```text
templates/medical-ai-test-plan-template.md
templates/medical-ai-test-specification-template.md
templates/medical-ai-change-impact-checklist.md
src/learn_ai_evaluation/medical_ai_splits.py
examples/medical-ai-evaluation/patient_level_split_example.py
```
