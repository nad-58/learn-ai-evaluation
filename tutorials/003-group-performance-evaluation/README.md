# 003 — Group Performance Evaluation

This chapter explains how to compare model results across different data groups.

Overall model performance can hide differences between groups. A model may perform well on average but less well for one subgroup.

## Basic workflow

1. Define the prediction task.
2. Identify the groups to compare.
3. Check the number of samples in each group.
4. Calculate the same metrics for each group.
5. Compare the results.
6. Investigate large differences.
7. Document findings and limitations.

## Dataset checks

Before comparing model results, check:

- sample count per group;
- missing values per group;
- label distribution per group;
- duplicate records;
- feature distribution differences;
- split separation between training and testing data.

## Simple numerical examples

Positive prediction rate:

```text
Group A: 300 positive predictions from 1000 samples = 0.30
Group B: 200 positive predictions from 800 samples = 0.25
Ratio = 0.30 / 0.25 = 1.20
```

True positive rate:

```text
Group A: 80 / (80 + 20) = 0.80
Group B: 60 / (60 + 40) = 0.60
Ratio = 0.80 / 0.60 = 1.33
```

False positive rate:

```text
Group A: 20 / (20 + 900) = 0.0217
Group B: 10 / (10 + 950) = 0.0104
Ratio = 0.0217 / 0.0104 = 2.09
```

## Key takeaway

Group-level evaluation should start with the dataset and continue through model testing, threshold review, and monitoring.
