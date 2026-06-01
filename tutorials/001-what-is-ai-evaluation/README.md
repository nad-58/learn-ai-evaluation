# 001 — What is AI Evaluation?

## Introduction

AI evaluation is the structured process of assessing whether an AI or machine learning system performs reliably for its intended task and operating conditions.

Traditional software is usually deterministic: the same input should produce the same output. Machine learning systems are different because they learn patterns from data. Their behaviour depends on the dataset, training process, model design, and the environment where they are used.

For this reason, AI evaluation should not only check whether the code runs. It should examine the data, the model, the integrated system, and the behaviour of the system over time.

## Why AI Evaluation Matters

A model can have high accuracy during development and still fail when used on new data. This can happen because of poor data quality, weak splitting strategy, label errors, class imbalance, distribution shift, or hidden performance gaps across subgroups.

A good evaluation process helps answer questions such as:

- Is the dataset suitable for the task?
- Are the training, validation, and test sets separated correctly?
- Are the selected metrics appropriate?
- Does the model generalise to unseen data?
- Does performance vary across important subgroups?
- Is the model stable under realistic input variation?
- Does the model work correctly when integrated into a larger pipeline?
- Is there a process for monitoring changes over time?

## Three Levels of AI Evaluation

AI evaluation can be organised into three main levels.

### 1. Data Evaluation

Data evaluation is the foundation of AI evaluation. A model cannot be reliable if the data is incomplete, inconsistent, biased, duplicated, or poorly labelled.

Typical checks include:

- missing values;
- duplicate records;
- label consistency;
- class imbalance;
- subgroup representation;
- train/test leakage;
- feature distribution;
- data preprocessing assumptions.

### 2. Model Evaluation

Model evaluation focuses on the behaviour of the trained model.

Typical checks include:

- classification, regression, or computer vision metrics;
- confusion matrix analysis;
- ROC and precision-recall analysis;
- calibration;
- subgroup performance;
- error analysis;
- robustness to realistic data variation;
- comparison with baseline models.

### 3. System-Level Evaluation

System-level evaluation examines how the model behaves after integration into a larger software or data pipeline.

Typical checks include:

- input validation;
- preprocessing consistency;
- API behaviour;
- latency and throughput;
- resource use;
- logging;
- data drift;
- prediction drift;
- re-evaluation after model updates.

## AI Evaluation Across the Lifecycle

AI evaluation should happen across the full AI lifecycle.

### Before Training

Before training, the focus is on data quality, data splitting, label quality, class distribution, leakage risk, and whether the dataset is suitable for the task.

### During Training

During training, the focus is on learning behaviour, including loss curves, overfitting, underfitting, convergence, and hyperparameter sensitivity.

### After Training

After training, the focus is on performance evaluation using independent test data, subgroup analysis, calibration, robustness checks, and error analysis.

### After Integration

After integration, the focus is on whether the model works correctly inside the larger system, including pipelines, APIs, latency, resource use, and monitoring.

### After Deployment

After deployment, the focus is on monitoring data drift, prediction drift, performance changes, and whether the model needs re-evaluation.

## Common AI Evaluation Challenges

AI evaluation is challenging because machine learning systems are statistical and data-dependent.

Common challenges include:

- lack of clear ground truth in some tasks;
- non-deterministic training behaviour;
- dependence on data quality;
- limited interpretability of some models;
- hidden subgroup performance differences;
- real-world data changes over time.

## Practical AI Evaluation Framework

A simple AI evaluation workflow can be:

```text
1. Define the task and intended use
2. Evaluate the dataset
3. Select appropriate metrics
4. Establish baseline performance
5. Evaluate the trained model
6. Analyse errors and subgroups
7. Test robustness under realistic variation
8. Review explainability and failure modes
9. Evaluate system-level integration
10. Monitor drift and performance over time
11. Re-evaluate after meaningful updates
```

## Key Takeaway

AI evaluation is not only about accuracy. It is a structured process for understanding data quality, model behaviour, robustness, fairness, system integration, and performance over time.
