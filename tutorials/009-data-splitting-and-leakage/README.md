# Data Splitting and Leakage

Data splitting is one of the most important parts of AI evaluation. A model should be tested on data that is independent from the data used to train or tune it.

This tutorial explains common leakage risks and practical checks for train, validation, and test splits.

## What is data leakage?

Data leakage occurs when information that should not be available during model training or inference influences the model. Leakage can produce overly optimistic evaluation results and make a model look better than it really is.

Leakage can happen through:

- duplicated records across splits
- the same subject or entity appearing in multiple splits
- preprocessing fitted before splitting
- target information embedded in features
- time leakage in temporal datasets
- near-duplicate images, text, or signals
- manual selection of test cases after seeing model performance

## Split units

The split unit should match the independence requirement of the evaluation.

For example:

- image-level split may be insufficient if multiple images come from the same subject
- row-level split may be insufficient if repeated measurements come from the same entity
- random split may be inappropriate for time-series forecasting
- file-level split may be insufficient if derived files share the same source

A good split design starts by identifying the unit that must not cross between training and test data.

## Common split strategies

### Random split

Useful for simple educational examples. It is not always appropriate for real-world evaluation because related records can be separated across splits.

### Stratified split

Maintains similar class proportions across splits. This is useful for classification tasks, especially with class imbalance.

### Group split

Keeps all records from the same group in the same split. Groups may be subjects, devices, sites, users, files, locations, or acquisition sessions.

### Temporal split

Uses earlier data for training and later data for testing. This is often more realistic for forecasting or deployment scenarios where the future differs from the past.

## Leakage checks

At minimum, check for exact overlap between train and test data using identifiers or selected feature columns.

This repository provides:

```python
split_leakage_report(train_df, test_df, columns=["sample_id"])
```

This exact check will not detect all leakage. Near-duplicate checks may require domain-specific methods such as image similarity, text similarity, signal similarity, or entity-resolution logic.

## Preprocessing leakage

Preprocessing should be fitted only on training data, then applied to validation and test data.

Examples of preprocessing that can leak information if fitted before splitting:

- scaling and normalisation
- imputation
- feature selection
- dimensionality reduction
- target encoding
- oversampling or synthetic sample generation

## Reporting split design

A dataset evaluation report should document:

- split method
- split ratios
- random seed if used
- split unit
- group identifier if used
- class balance per split
- leakage checks performed
- known residual leakage risks

## Key lesson

A model evaluation result is only credible when the test data is independent from training and tuning decisions. Leakage control is therefore part of evaluation design, not only data preparation.
