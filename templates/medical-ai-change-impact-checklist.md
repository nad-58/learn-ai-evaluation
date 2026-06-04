# Medical AI Change Impact Checklist

This checklist supports public-safe technical review of changes to health-related AI systems. It is educational and does not define official requirements.

## 1. Change summary

**Change ID:**  
**Date:**  
**AI function affected:**  
**Previous version:**  
**New version:**  
**Change owner:**  
**Reviewer:**  

Describe the change in plain language.

## 2. Change category

Select all that apply.

- [ ] Model retraining
- [ ] New training data
- [ ] Removed training data
- [ ] Label or reference update
- [ ] Model architecture change
- [ ] Hyperparameter change
- [ ] Decision-threshold change
- [ ] Calibration update
- [ ] Preprocessing change
- [ ] Post-processing change
- [ ] Explainability method change
- [ ] Software dependency update
- [ ] Runtime environment change
- [ ] Data source change
- [ ] Acquisition protocol change
- [ ] User-interface change
- [ ] Monitoring rule change
- [ ] Documentation-only change
- [ ] Other

## 3. Impact questions

| Question | Yes / No / Unknown | Notes |
|---|---|---|
| Could the change affect model inputs? |  |  |
| Could the change affect model outputs? |  |  |
| Could the change affect thresholds or decisions? |  |  |
| Could the change affect calibration? |  |  |
| Could the change affect subgroup performance? |  |  |
| Could the change affect robustness to input variation? |  |  |
| Could the change affect failure modes? |  |  |
| Could the change affect integration with other components? |  |  |
| Could the change affect user interpretation? |  |  |
| Could the change affect monitoring signals? |  |  |

## 4. Evidence reviewed

| Evidence item | Version / location | Reviewed by | Notes |
|---|---|---|---|
| Dataset summary |  |  |  |
| Training report |  |  |  |
| Evaluation report |  |  |  |
| Split and leakage report |  |  |  |
| Subgroup report |  |  |  |
| Failure-case review |  |  |  |
| Back-to-back comparison |  |  |  |
| Software verification evidence |  |  |  |

## 5. Recommended re-testing level

Select one and justify the rationale.

- [ ] No re-testing proposed
- [ ] Targeted re-testing proposed
- [ ] Full technical re-testing proposed
- [ ] Additional data collection proposed
- [ ] Independent review proposed

**Rationale:**  

## 6. Back-to-back comparison

Use this section when comparing the previous and new versions on the same fixed dataset.

| Comparison item | Result | Notes |
|---|---:|---|
| Number of samples compared |  |  |
| Number of changed binary decisions |  |  |
| Mean absolute score difference |  |  |
| Largest score difference |  |  |
| Subgroup with largest change |  |  |
| New false positives |  |  |
| New false negatives |  |  |
| Improved previous failures |  |  |

## 7. Release decision

**Decision:** Accept / reject / defer / request more evidence  
**Decision owner:**  
**Decision date:**  
**Conditions or follow-up actions:**  

## 8. Rollback and monitoring

**Rollback plan:**  
**Monitoring signals to review:**  
**Trigger for re-evaluation:**  
**Review frequency:**  

## 9. Public-safe checklist

- [ ] No confidential data is included.
- [ ] No personal data is included.
- [ ] No proprietary screenshots or outputs are included.
- [ ] The change rationale is documented.
- [ ] The re-testing decision is justified.
- [ ] Limitations are stated clearly.
