# Medical AI Test Specification Template

This template defines detailed test cases for technical evaluation of health-related AI examples. It is public-safe and educational.

## 1. Test identification

**Test ID:**  
**Test name:**  
**AI function under test:**  
**Version:**  
**Related test plan:**  
**Prepared by:**  
**Date:**  

## 2. Test objective

Describe the specific behaviour being evaluated. The objective should be measurable and linked to a defined metric, dataset, or scenario.

## 3. Preconditions

List the required state before the test is executed.

- Model version is fixed.
- Test dataset is available and access-controlled.
- Test split is separated from training and tuning data.
- Test environment is configured.
- Metric script version is recorded.
- Thresholds and post-processing rules are defined.

## 4. Input data

| Data item | Description | Source | Version | Notes |
|---|---|---|---|---|
| Test dataset |  |  |  |  |
| Labels / reference |  |  |  |  |
| Metadata |  |  |  |  |

## 5. Data independence and leakage checks

| Check | Result | Evidence location | Notes |
|---|---|---|---|
| Patient or subject overlap across splits |  |  |  |
| Duplicate or near-duplicate samples |  |  |  |
| Repeated scans or longitudinal samples |  |  |  |
| Preprocessing fitted only on training data |  |  |  |
| Hyperparameter tuning separated from final test |  |  |  |
| Test set reused during development |  |  |  |

## 6. Test procedure

| Step | Action | Expected output | Evidence |
|---:|---|---|---|
| 1 | Load model and configuration | Model loads without error |  |
| 2 | Load test dataset | Dataset count matches specification |  |
| 3 | Run preprocessing | Inputs match expected format |  |
| 4 | Run model inference | Scores, masks, boxes, or measurements are produced |  |
| 5 | Run post-processing | Final outputs are produced |  |
| 6 | Calculate metrics | Metric report is generated |  |
| 7 | Review failures | Failure-case summary is produced |  |

## 7. Acceptance or decision criteria

| Criterion ID | Metric or condition | Target | Result | Pass / concern |
|---|---|---:|---:|---|
| AC-001 |  |  |  |  |
| AC-002 |  |  |  |  |

## 8. Subgroup evaluation

| Grouping variable | Group | Count | Metric 1 | Metric 2 | Notes |
|---|---|---:|---:|---:|---|
|  |  |  |  |  |  |

## 9. Robustness and edge cases

| Scenario | Reason for inclusion | Expected behaviour | Observed behaviour | Notes |
|---|---|---|---|---|
| Low-quality input |  |  |  |  |
| Missing metadata |  |  |  |  |
| Borderline case |  |  |  |  |
| Different site or scanner |  |  |  |  |
| Out-of-distribution input |  |  |  |  |

## 10. Deviations

Record any deviation from the planned test procedure.

| Deviation ID | Description | Impact assessment | Approved by |
|---|---|---|---|
| DEV-001 |  |  |  |

## 11. Result summary

Summarise the result, limitations, and recommended next action. Avoid over-claiming beyond the technical evidence.
