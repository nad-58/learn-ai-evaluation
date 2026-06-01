# Model Evaluation Report Template

## 1. Model Overview

- Model name:
- Model version:
- Task type:
- Input data:
- Output:
- Intended use:
- Evaluation date:

## 2. Dataset Summary

- Training dataset:
- Validation dataset:
- Test dataset:
- Data sources:
- Number of samples:
- Number of classes:
- Missing data:
- Duplicates:
- Class balance:
- Subgroup coverage:

## 3. Data Splitting Strategy

- Split method:
- Split unit:
- Leakage prevention method:
- Rationale:

## 4. Evaluation Metrics

List the selected metrics and explain why they are appropriate.

| Metric | Purpose | Result | Target |
|---|---|---:|---:|
| Accuracy | Overall correctness |  |  |
| Precision | Positive prediction quality |  |  |
| Recall | Positive case detection |  |  |
| F1-score | Balance between precision and recall |  |  |

## 5. Performance Results

Summarise performance on validation and test data.

## 6. Subgroup Evaluation

Report performance across relevant subgroups.

| Subgroup | Sample Size | Metric 1 | Metric 2 | Notes |
|---|---:|---:|---:|---|
|  |  |  |  |  |

## 7. Robustness Evaluation

Describe tests performed under noise, perturbation, edge cases, or distribution shift.

## 8. Error Analysis

Describe the main types of errors and where they occur.

## 9. Explainability and Model Behaviour

Summarise any explainability analysis or feature importance review.

## 10. System-Level Considerations

- Latency:
- Throughput:
- Resource usage:
- API behaviour:
- Pipeline checks:
- Monitoring plan:

## 11. Limitations

List known limitations, assumptions, and areas requiring future evaluation.

## 12. Conclusion

Provide a clear summary of whether the model performance is suitable for the intended task.
