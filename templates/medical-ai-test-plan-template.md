# Medical AI Test Plan Template

This template supports public-safe technical evaluation planning for health-related AI examples. It is not a clinical validation template and it does not define official regulatory requirements.

## 1. Test plan summary

**Project name:**  
**AI function under test:**  
**Model or system version:**  
**Date:**  
**Prepared by:**  
**Review status:** Draft / reviewed / approved  

Briefly describe the AI function, why it is being tested, and what evidence the test plan is expected to produce.

## 2. AI function boundary

**Input data:**  
**Output data:**  
**Pre-processing included:** Yes / No  
**Post-processing included:** Yes / No  
**Decision threshold included:** Yes / No / not applicable  
**User interface included:** Yes / No  
**System integration included:** Yes / No  
**Out-of-scope functions:**  

## 3. Test objectives

| Objective ID | Objective | Primary metric | Decision criterion | Lifecycle stage |
|---|---|---|---|---|
| OBJ-001 |  |  |  |  |
| OBJ-002 |  |  |  |  |

## 4. Test scope

Describe what the test includes and excludes. Include model-level, component-level, system-level, and monitoring-level boundaries where relevant.

## 5. Roles and responsibilities

| Role | Responsibility | Named owner | Independence considerations |
|---|---|---|---|
| Test owner |  |  |  |
| Data owner |  |  |  |
| Model owner |  |  |  |
| Metric reviewer |  |  |  |
| Domain reviewer |  |  |  |
| Quality reviewer |  |  |  |

## 6. Test environment

| Item | Description | Version / configuration | Notes |
|---|---|---|---|
| Hardware |  |  |  |
| Operating system |  |  |  |
| Python version |  |  |  |
| Main libraries |  |  |  |
| Model file / checkpoint |  |  |  |
| Pre-processing pipeline |  |  |  |
| Post-processing pipeline |  |  |  |
| Thresholds |  |  |  |
| Random seeds |  |  |  |

## 7. Test data plan

**Dataset source:**  
**Number of samples:**  
**Number of independent entities:**  
**Independence unit:** Patient / subject / study / scan / site / scanner / episode / other  
**Inclusion criteria:**  
**Exclusion criteria:**  
**Label or reference source:**  
**Data split method:**  
**Leakage checks:**  
**Subgroup variables:**  

## 8. Test methods

Select the methods relevant to this evaluation.

- [ ] Classification metrics
- [ ] Segmentation metrics
- [ ] Detection metrics
- [ ] Regression or measurement metrics
- [ ] Threshold analysis
- [ ] Calibration analysis
- [ ] Subgroup performance analysis
- [ ] Robustness testing
- [ ] Failure-case review
- [ ] Back-to-back comparison
- [ ] System integration testing
- [ ] Monitoring review

## 9. Acceptance or decision criteria

Document the predefined criteria used to interpret the test. Avoid changing criteria after reviewing final test results.

| Criterion ID | Criterion | Rationale | Applies to |
|---|---|---|---|
| AC-001 |  |  |  |
| AC-002 |  |  |  |

## 10. Deliverables

| Deliverable | Owner | Due date | Review status |
|---|---|---|---|
| Dataset summary |  |  |  |
| Split and leakage report |  |  |  |
| Metric report |  |  |  |
| Subgroup report |  |  |  |
| Failure-case summary |  |  |  |
| Final test report |  |  |  |

## 11. Re-testing plan

Describe what type of change would trigger re-testing and whether full or partial re-testing is expected.

## 12. Limitations

State known limitations of the test plan, including dataset limitations, subgroup limitations, environmental limitations, and uncertainty in reference labels.
