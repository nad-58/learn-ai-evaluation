# Medical AI Evaluation Report Template

This template is for public-safe technical evaluation of medical or health-related AI examples. It is not a clinical validation template and it does not define regulatory, clinical, or legal requirements.

## 1. Evaluation summary

**Project name:**  
**Model or system version:**  
**Evaluation date:**  
**Evaluation owner:**  
**Task type:** Binary classification / multi-class classification / segmentation / detection / risk scoring / other  
**Evaluation status:** Exploratory / locked protocol / final technical test / monitoring review  

Provide a short summary of what was evaluated, what dataset was used, what the main result was, and what limitations should be understood before interpreting the result.

## 2. Intended technical task

Describe the technical task clearly. Avoid vague statements such as "the model diagnoses disease" unless the project has appropriate clinical validation and governance. For a technical evaluation report, use precise wording such as:

- The model predicts whether a target finding is present in the input.
- The model segments a region of interest in an image.
- The model produces a risk score for a predefined endpoint.
- The model detects candidate objects or regions for further review.

**Input type:**  
**Output type:**  
**Target label or reference standard:**  
**Decision threshold:**  
**Human user role, if applicable:**  
**Known non-goals or out-of-scope uses:**  

## 3. Dataset description

Describe the evaluation dataset in enough detail that another reviewer can understand its relevance and limitations.

**Dataset source:** Synthetic / public / internal non-confidential / other  
**Number of cases:**  
**Number of positive cases:**  
**Number of negative cases:**  
**Class balance:**  
**Data split method:**  
**Independence unit:** Patient / subject / study / image / video / scan / encounter / other  
**Duplicate and leakage checks performed:**  
**Missing data checks performed:**  
**Inclusion criteria:**  
**Exclusion criteria:**  

### Subgroup coverage

| Subgroup variable | Groups included | Count per group | Why this grouping matters | Limitations |
|---|---:|---:|---|---|
| Site / source |  |  |  |  |
| Acquisition device / scanner |  |  |  |  |
| Protocol / setting |  |  |  |  |
| Image quality band |  |  |  |  |
| Demographic grouping, if justified and appropriate |  |  |  |  |

## 4. Evaluation protocol

State whether the evaluation protocol was fixed before the final test. If threshold selection, subgroup analysis, or failure review was performed after looking at the test set, describe this transparently.

**Protocol locked before final test:** Yes / No  
**Threshold locked before final test:** Yes / No  
**Primary metric:**  
**Secondary metrics:**  
**Minimum acceptable technical target, if defined:**  
**Statistical uncertainty method, if used:**  
**Number of repeated runs, if applicable:**  

## 5. Binary classification metrics

Use this section for binary classification or binary decision tasks.

| Metric | Value | Notes |
|---|---:|---|
| True positives |  |  |
| False positives |  |  |
| True negatives |  |  |
| False negatives |  |  |
| Sensitivity / recall |  |  |
| Specificity |  |  |
| Precision / PPV |  |  |
| Negative predictive value |  |  |
| Accuracy |  |  |
| Balanced accuracy |  |  |
| F1 score |  |  |
| False positive rate |  |  |
| False negative rate |  |  |

### Threshold analysis

| Threshold | Sensitivity | Specificity | Precision / PPV | False positive rate | False negative rate | Notes |
|---:|---:|---:|---:|---:|---:|---|
|  |  |  |  |  |  |  |

Explain why the selected threshold was chosen and whether it was selected before or after final test evaluation.

## 6. Calibration review

Use this section when the model output is interpreted as a probability or risk score.

| Score bin | Number of cases | Mean predicted score | Observed event rate | Absolute gap |
|---|---:|---:|---:|---:|
| 0.0–0.2 |  |  |  |  |
| 0.2–0.4 |  |  |  |  |
| 0.4–0.6 |  |  |  |  |
| 0.6–0.8 |  |  |  |  |
| 0.8–1.0 |  |  |  |  |

**Expected calibration error:**  
**Calibration limitations:**  

## 7. Segmentation or measurement evaluation

Use this section for segmentation, measurement, or region-of-interest tasks.

| Metric | Value | Notes |
|---|---:|---|
| Dice score |  |  |
| IoU |  |  |
| Pixel / voxel accuracy |  |  |
| Reference volume |  |  |
| Predicted volume |  |  |
| Absolute volume difference |  |  |
| Relative volume difference |  |  |

Describe whether the errors are small boundary differences, missing regions, extra regions, or systematic under/over-estimation.

## 8. Subgroup performance

| Grouping variable | Group | Count | Sensitivity | Specificity | Precision / PPV | Balanced accuracy | Notes |
|---|---|---:|---:|---:|---:|---:|---|
|  |  |  |  |  |  |  |  |

Discuss whether subgroup results are stable enough to interpret. Avoid over-interpreting very small groups. Where relevant, report confidence intervals or repeat the analysis on a larger dataset.

## 9. Robustness and stress testing

Describe how the model behaves under realistic input variation.

| Test condition | Expected behaviour | Observed behaviour | Pass / concern | Notes |
|---|---|---|---|---|
| Lower image quality |  |  |  |  |
| Different acquisition source |  |  |  |  |
| Missing or incomplete metadata |  |  |  |  |
| Borderline cases |  |  |  |  |
| Out-of-distribution examples |  |  |  |  |

## 10. Failure-case review

Summarise the main types of errors. Include anonymised and public-safe examples only.

| Failure type | Example pattern | Frequency | Possible cause | Follow-up action |
|---|---|---:|---|---|
| False positive |  |  |  |  |
| False negative |  |  |  |  |
| Poor calibration |  |  |  |  |
| Segmentation boundary error |  |  |  |  |
| Subgroup-specific issue |  |  |  |  |

## 11. System-level considerations

A model may perform well in isolation but behave differently after integration. Record any system-level assumptions here.

**Pre-processing assumptions:**  
**Post-processing assumptions:**  
**User interface assumptions:**  
**Human review assumptions:**  
**Runtime environment:**  
**Known integration risks:**  

## 12. Lifecycle and monitoring plan

Define what should be monitored after deployment or after repeated use in a new environment.

| Monitoring item | Signal | Review frequency | Trigger for re-evaluation | Owner |
|---|---|---|---|---|
| Input data distribution |  |  |  |  |
| Output score distribution |  |  |  |  |
| Error reports |  |  |  |  |
| Subgroup performance |  |  |  |  |
| Calibration |  |  |  |  |
| Software or model changes |  |  |  |  |

## 13. Limitations

State limitations clearly. Example limitations may include small sample size, limited subgroup coverage, synthetic data, single-site data, missing edge cases, uncertain reference labels, lack of temporal validation, or no independent external dataset.

## 14. Conclusion

Provide a balanced conclusion. Avoid over-claiming. State what the evaluation supports, what it does not support, and what evidence would be needed next.

## 15. Public-safe checklist

- [ ] No confidential client or project information is included.
- [ ] No personal data is included.
- [ ] No proprietary datasets are exposed.
- [ ] No clinical claims are made without appropriate evidence.
- [ ] Synthetic or public data is clearly labelled.
- [ ] Limitations are clearly stated.
- [ ] Threshold selection is documented.
- [ ] Subgroup counts are reported.
- [ ] Failure cases are anonymised or synthetic.
- [ ] Lifecycle monitoring triggers are described.
