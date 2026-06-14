# Dataset Evaluation

Dataset evaluation should happen before model training and before model metrics are interpreted. A model can appear strong while relying on duplicated records, leakage, missing values, invalid ranges, class imbalance, or weak labels.

## Runnable Python examples

Run these commands from the repository root:

```bash
python examples/dataset-evaluation/missing_values_and_duplicates_example.py
python examples/dataset-evaluation/class_balance_and_distributions_example.py
python examples/dataset-evaluation/outliers_and_leakage_example.py
python examples/dataset-evaluation/dataset_quality_example.py
```

| Example | What it demonstrates |
|---|---|
| [`missing_values_and_duplicates_example.py`](../../examples/dataset-evaluation/missing_values_and_duplicates_example.py) | Missing counts, missing percentages, and duplicate identifiers |
| [`class_balance_and_distributions_example.py`](../../examples/dataset-evaluation/class_balance_and_distributions_example.py) | Class proportions, numerical summaries, and categorical cardinality |
| [`outliers_and_leakage_example.py`](../../examples/dataset-evaluation/outliers_and_leakage_example.py) | IQR outlier screening and train/test overlap |
| [`dataset_quality_example.py`](../../examples/dataset-evaluation/dataset_quality_example.py) | Complete end-to-end dataset-quality report |

Reusable utilities:

```text
src/learn_ai_evaluation/dataset_quality.py
```

## 1. Missing values

For each column, report missing count and percentage:

```text
missing percentage = missing count / total rows × 100
```

Python example:

```python
import pandas as pd
from learn_ai_evaluation.dataset_quality import missing_value_report

records = pd.DataFrame(
    {
        "age": [25, 41, None, None, 63, 52],
        "score": [0.72, 0.81, 0.66, 0.66, None, 0.73],
    }
)

print(missing_value_report(records))
```

Expected interpretation:

```text
age:   2/6 missing = 33.33%
score: 1/6 missing = 16.67%
```

Missingness should also be examined by site, class, time period, and subgroup. Imputation must be fitted only using training data.

## 2. Duplicate records

Check duplicates using all columns and important identifiers such as subject ID, sample ID, filename, or image ID.

```python
import pandas as pd
from learn_ai_evaluation.dataset_quality import duplicate_report

records = pd.DataFrame(
    {
        "sample_id": ["s1", "s2", "s3", "s3", "s4"],
        "label": [0, 0, 1, 1, 0],
    }
)

print(duplicate_report(records, subset=["sample_id"]))
```

Because `s3` appears twice, both rows are marked as duplicate rows.

## 3. Class balance

Report class counts and percentages. Imbalance affects metric choice, threshold selection, weighting, and confidence in minority-class performance.

```python
import pandas as pd
from learn_ai_evaluation.dataset_quality import class_balance_report

records = pd.DataFrame({"label": [0, 0, 0, 0, 0, 0, 0, 1, 1, 1]})
print(class_balance_report(records, target_column="label"))
```

Expected result:

```text
class 0: 7 rows = 70%
class 1: 3 rows = 30%
```

## 4. Numerical feature distributions

Review count, mean, standard deviation, minimum, quartiles, median, and maximum.

```python
import pandas as pd
from learn_ai_evaluation.dataset_quality import feature_distribution_report

records = pd.DataFrame(
    {
        "age": [22, 25, 31, 38, 41, 52, 63, 70],
        "score": [0.42, 0.55, 0.61, 0.67, 0.72, 0.78, 0.84, 0.91],
    }
)

print(feature_distribution_report(records, numeric_columns=["age", "score"]))
```

Compare these statistics across training, validation, test, subgroup, and deployment datasets.

## 5. Categorical cardinality

Check unique values, missing categories, rare categories, spelling differences, and unseen deployment categories.

```python
import pandas as pd
from learn_ai_evaluation.dataset_quality import categorical_cardinality_report

records = pd.DataFrame({"site": ["A", "A", "B", "B", "C", None]})
print(categorical_cardinality_report(records, categorical_columns=["site"]))
```

This example has three observed categories and one missing value.

## 6. Potential outliers

The example uses the interquartile-range rule:

```text
IQR = Q3 - Q1
lower = Q1 - 1.5 × IQR
upper = Q3 + 1.5 × IQR
```

```python
import pandas as pd
from learn_ai_evaluation.dataset_quality import outlier_report_iqr

records = pd.DataFrame({"age": [24, 27, 31, 35, 39, 42, 46, 120]})
print(outlier_report_iqr(records, numeric_columns=["age"]))
```

The value `120` is screened as a potential outlier. An outlier is not automatically an error and should be investigated before removal.

## 7. Train/test leakage

Check whether the same entity or record appears in train, validation, and test data.

```python
import pandas as pd
from learn_ai_evaluation.dataset_quality import split_leakage_report

train = pd.DataFrame({"sample_id": ["s1", "s2", "s3", "s4", "s5"]})
test = pd.DataFrame({"sample_id": ["s5", "s6", "s7"]})

print(split_leakage_report(train, test, columns=["sample_id"]))
```

Expected result:

```text
overlapping rows: 1
overlap percentage of test: 33.33%
```

The shared identifier `s5` means the split must be corrected.

Common leakage sources include duplicate records, repeated measurements from one person, preprocessing fitted on all data, target-derived features, and future information used in historical prediction.

## 8. Complete end-to-end report

Run:

```bash
python examples/dataset-evaluation/dataset_quality_example.py
```

The complete example prints:

1. missing-value report;
2. duplicate report;
3. class-balance report;
4. numerical distribution report;
5. categorical-cardinality report;
6. potential outliers;
7. split-overlap results;
8. a generated Markdown report.

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
