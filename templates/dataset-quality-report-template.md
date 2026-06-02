# Dataset Quality Report Template

## 1. Dataset overview

- Dataset name:
- Task type:
- Target variable:
- Number of rows:
- Number of columns:
- Data source:
- Collection period:
- Intended evaluation use:

## 2. Dataset scope

Describe what the dataset represents and what it does not represent.

Include:

- inclusion criteria
- exclusion criteria
- expected use context
- known limitations
- expected deployment mismatch

## 3. Missing values

| Column | Missing count | Missing percent | Action | Rationale |
|---|---:|---:|---|---|
|  |  |  |  |  |

Review questions:

- Are missing values random or systematic?
- Are missing values concentrated in a subgroup, source, site, or time period?
- Could missingness itself be predictive of the target?
- Has imputation been fitted only on training data?

## 4. Duplicates

| Duplicate type | Check performed | Result | Action |
|---|---|---|---|
| Exact row duplicate |  |  |  |
| Identifier duplicate |  |  |  |
| Entity-level duplicate |  |  |  |
| Near-duplicate |  |  |  |

Review questions:

- Do duplicate or near-duplicate records cross train, validation, and test splits?
- Are repeated records legitimate repeated measurements?
- What unit should be kept independent across splits?

## 5. Class balance and label distribution

| Class | Count | Percent | Notes |
|---|---:|---:|---|
|  |  |  |  |

Review questions:

- Is the minority class large enough for reliable evaluation?
- Are class proportions similar across train, validation, and test splits?
- Are additional metrics needed beyond accuracy?

## 6. Feature distribution

Summarise key numeric and categorical features.

| Feature | Type | Summary | Concern | Action |
|---|---|---|---|---|
|  |  |  |  |  |

Review questions:

- Are feature ranges plausible?
- Are there unexpected values or coding errors?
- Are categorical values consistent?
- Are high-cardinality variables handled appropriately?

## 7. Potential outliers

| Feature | Outlier rule | Count | Percent | Decision |
|---|---|---:|---:|---|
|  |  |  |  |  |

Outliers should be reviewed before removal. They may represent rare but valid cases, measurement errors, or deployment edge cases.

## 8. Data splitting and leakage

- Split method:
- Split ratio:
- Random seed:
- Split unit:
- Group variable, if applicable:
- Temporal split, if applicable:

| Leakage check | Columns or unit used | Result | Action |
|---|---|---|---|
| Exact overlap |  |  |  |
| Identifier overlap |  |  |  |
| Group overlap |  |  |  |
| Near-duplicate review |  |  |  |

## 9. Representativeness

Describe whether the dataset covers the expected variation in real use.

Consider:

- source or site diversity
- demographic or subgroup coverage, where relevant and appropriate
- device or acquisition variation
- time period coverage
- environmental or operational conditions
- edge cases and rare cases

## 10. Dataset documentation conclusion

Overall dataset quality decision:

- Suitable for evaluation:
- Suitable with limitations:
- Not suitable without remediation:

Summary of required actions before model evaluation:

1.
2.
3.
