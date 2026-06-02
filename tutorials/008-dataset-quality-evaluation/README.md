# Dataset Quality Evaluation

Dataset evaluation is the first checkpoint before trusting any model result. A model score is only meaningful if the data used to train, validate, and test the model has been checked for quality problems.

This tutorial focuses on practical checks that should be performed before model training:

- missing values
- duplicated records
- class imbalance
- label distribution
- feature distribution
- categorical cardinality
- potential outliers
- dataset documentation

## Why dataset quality matters

A high model score can be misleading when the dataset contains hidden issues. Missing values may be random, but they may also reflect a systematic collection problem. Duplicates can inflate performance when the same or near-identical samples appear in both training and test data. Class imbalance can make accuracy look strong while the model performs poorly on the minority class.

Dataset evaluation is not only data cleaning. It is an evidence-gathering step that helps decide whether the dataset is suitable for the intended evaluation.

## Missing values

Missing values should be reported per column as both count and percentage. A useful review question is whether the missingness is random or concentrated in a subgroup, data source, site, time period, or measurement condition.

Typical actions include:

- report missingness before imputation
- check whether missing values are associated with the target label
- avoid using the target label to decide how to impute features
- document any exclusion or imputation rule

## Duplicates

Duplicates can occur at different levels. A row may be exactly duplicated, but the same real-world entity may also appear multiple times with small differences.

Examples of duplication checks include:

- exact row duplicates
- duplicate sample identifiers
- duplicate filenames or acquisition IDs
- repeated records from the same subject or entity
- near-duplicates in images, text, or time series

Duplicates are especially important when creating train, validation, and test splits.

## Class imbalance

Class imbalance means that one or more target classes are under-represented. Accuracy can be misleading in this situation. For example, if 95% of samples belong to one class, a model can achieve 95% accuracy by always predicting that class.

For imbalanced classification, consider reporting metrics such as precision, recall, F1-score, balanced accuracy, sensitivity, specificity, ROC-AUC, or PR-AUC depending on the task.

## Feature distribution

Numeric feature summaries help identify unexpected ranges, measurement errors, distribution shifts, and extreme values. Useful statistics include minimum, maximum, mean, standard deviation, median, and quartiles.

Categorical feature summaries should include missingness, number of unique values, and most common categories. Very high-cardinality categorical features may require special handling.

## Outliers

Outliers should not be removed automatically. They may represent:

- data entry errors
- rare but valid cases
- new operating conditions
- important edge cases for deployment

The IQR rule is a simple screening method. It should be used to flag records for review, not as an automatic deletion rule.

## Practical Python utilities

This repository provides utilities in:

```text
src/learn_ai_evaluation/dataset_quality.py
```

Main functions:

```python
missing_value_report(df)
duplicate_report(df, subset=None)
class_balance_report(df, target_column="label")
feature_distribution_report(df)
categorical_cardinality_report(df)
outlier_report_iqr(df)
render_markdown_report(df, target_column="label")
```

A runnable example is available at:

```text
examples/dataset-evaluation/dataset_quality_example.py
```

## Review checklist

Before using a dataset for model evaluation, document:

- dataset source and collection period
- inclusion and exclusion rules
- target label definition
- missing-value handling
- duplicate handling
- train, validation, and test split method
- class distribution in each split
- known limitations and expected deployment mismatch

## Key lesson

A dataset quality report should be created before model performance is reported. Otherwise, model metrics may hide preventable data problems.
