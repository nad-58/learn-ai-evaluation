# Dataset Evaluation

Dataset evaluation should happen before model training and before model metrics are interpreted. A model can appear strong while relying on duplicated records, leakage, missing values, invalid ranges, class imbalance, or weak labels.

## Run the example

```bash
python examples/dataset-evaluation/dataset_quality_example.py
```

Reusable utilities:

```text
src/learn_ai_evaluation/dataset_quality.py
```

Runnable example:

```text
examples/dataset-evaluation/dataset_quality_example.py
```

## Checks included

### Missing values

For each column, report missing count and percentage:

```text
missing percentage = missing count / total rows × 100
```

Use:

```python
missing_value_report(df)
```

### Duplicates

Check duplicates using all columns and important identifiers such as subject ID, sample ID, filename, or image ID.

```python
duplicate_report(df, subset=["sample_id"])
```

### Class balance

Report class counts and percentages. Imbalance affects metric choice, threshold selection, weighting, and confidence in minority-class performance.

```python
class_balance_report(df, target_column="label")
```

### Numeric feature distributions

Review count, mean, standard deviation, minimum, quartiles, median, and maximum.

```python
feature_distribution_report(df, numeric_columns=["age", "score"])
```

### Categorical features

Check unique values, missing categories, rare categories, spelling differences, and unseen deployment categories.

```python
categorical_cardinality_report(df, categorical_columns=["site"])
```

### Potential outliers

The example uses the interquartile-range rule:

```text
IQR = Q3 - Q1
lower = Q1 - 1.5 × IQR
upper = Q3 + 1.5 × IQR
```

```python
outlier_report_iqr(df, numeric_columns=["age", "score"])
```

An outlier is not automatically an error. It should be investigated before removal.

### Split leakage

Check whether the same entity or record appears in train, validation, and test data.

```python
split_leakage_report(train_df, test_df, columns=["sample_id"])
```

Common leakage sources include duplicate records, repeated measurements from one person, preprocessing fitted on all data, target-derived features, and future information used in historical prediction.

## Worked synthetic dataset

The example contains 10 rows and deliberately includes:

- missing values;
- one duplicated identifier;
- imbalanced labels;
- an extreme age value;
- numeric and categorical features;
- a train/test split for leakage checking.

The script prints:

1. missing-value report;
2. duplicate report;
3. class-balance report;
4. numeric distribution report;
5. categorical-cardinality report;
6. potential outliers;
7. split-overlap results;
8. a Markdown report preview.

## Additional checks for real projects

Real projects may also require:

- subject-level split enforcement;
- image similarity or perceptual-hash checks;
- time-aware leakage checks;
- subgroup coverage analysis;
- annotation agreement and adjudication review;
- provenance, consent, privacy, and security review;
- dataset and label version control;
- comparison between training and deployment distributions.

## Decision

Dataset evaluation should end with a documented decision:

```text
acceptable
acceptable with limitations
remediation required
unsuitable for intended use
```
