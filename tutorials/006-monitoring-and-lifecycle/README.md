# Monitoring and Lifecycle Evaluation

An AI system can perform well during validation and still become unreliable later. Input data, prevalence, users, workflows, devices, software dependencies, labels, thresholds, and operating conditions can all change after release.

Monitoring and lifecycle evaluation determines whether current behaviour remains consistent with the approved baseline and whether routine operation, increased monitoring, investigation, mitigation, retraining, or full re-validation is required.

## Runnable examples

Run from the repository root:

```bash
python examples/monitoring-and-lifecycle/threshold_example.py
python examples/monitoring-and-lifecycle/drift_example.py
python examples/monitoring-and-lifecycle/monitoring_lifecycle_example.py
```

Run the tests:

```bash
python -m pytest tests/test_monitoring_lifecycle.py -q
```

Reusable utilities:

```text
src/learn_ai_evaluation/monitoring_lifecycle.py
```

## 1. Define the monitoring baseline

A baseline should be linked to a specific approved system state:

```text
model version
software version
preprocessing version
dataset version
thresholds
operating environment
reference time window
approved intended use
```

Without a traceable baseline, later changes cannot be interpreted reliably.

## 2. Define monitoring windows

Typical windows include:

- daily or weekly operational summaries;
- monthly performance reviews;
- rolling windows such as the latest 1,000 cases;
- event-triggered reviews after an incident or update;
- periodic external validation.

Record the start date, end date, sample count, label availability, subgroup coverage, and data completeness for every window.

## 3. Monitor model performance

For binary classification, useful periodic metrics include:

```text
sample count
prevalence
accuracy
precision
recall
F1
AUROC
```

Run:

```python
from learn_ai_evaluation.monitoring_lifecycle import binary_classification_metrics

metrics = binary_classification_metrics(
    y_true=[0, 0, 1, 1],
    y_score=[0.1, 0.2, 0.8, 0.9],
)
print(metrics)
```

Performance monitoring should also include subgroup and operating-condition results where relevant. Aggregate stability can hide degradation in one group or environment.

## 4. Threshold rules

A threshold rule should specify:

```text
metric
warning threshold
action threshold
direction
owner
required response
```

Example:

```python
from learn_ai_evaluation.monitoring_lifecycle import ThresholdRule

rule = ThresholdRule(
    metric="recall",
    warning=0.72,
    action=0.68,
    direction="lower_is_worse",
)
```

Interpretation:

```text
recall > 0.72        -> pass
0.68 < recall <= .72 -> warning
recall <= 0.68       -> action required
```

Run the numerical example:

```bash
python examples/monitoring-and-lifecycle/threshold_example.py
```

The example evaluates AUROC, recall, and precision and produces a lifecycle decision.

## 5. Data drift

Drift means that the current data distribution differs from the reference distribution. Drift can occur without immediate performance degradation, but it may indicate that the system is operating outside its validated conditions.

The repository implements Population Stability Index for numerical features:

```text
PSI = sum((current proportion - reference proportion)
          × ln(current proportion / reference proportion))
```

Run:

```bash
python examples/monitoring-and-lifecycle/drift_example.py
```

The example compares reference and current values for `age` and `score` and produces a feature-level drift report.

A PSI threshold is only a screening rule. It should not be treated as universal proof of harmful drift. Interpretation depends on feature meaning, sample size, binning, data quality, intended use, and model sensitivity.

## 6. Other monitoring signals

A production monitoring plan may include:

### Input signals

- missing-value rate;
- invalid or out-of-range inputs;
- new categorical values;
- sensor quality;
- image resolution or acquisition changes;
- prompt length or language changes;
- feature-distribution drift;
- source, site, device, and subgroup mix.

### Output signals

- prediction distribution;
- confidence distribution;
- abstention rate;
- positive-decision rate;
- anomaly rate;
- unsupported-claim or hallucination rate;
- tool-use failure rate for agents.

### Performance signals

- task metrics when labels become available;
- subgroup and worst-group performance;
- calibration;
- error severity;
- disagreement with human reviewers;
- near-miss and incident rate.

### Operational signals

- latency;
- throughput;
- availability;
- timeout rate;
- resource consumption;
- dependency failure;
- fallback or human-escalation rate.

## 7. Lifecycle decision logic

The repository uses a transparent hierarchy:

```text
action threshold crossed
-> re-evaluation or mitigation required

no action threshold, but drift review flag
-> data-shift review required

warning threshold crossed
-> increased monitoring required

no warning or drift flag
-> continue routine monitoring
```

Use:

```python
from learn_ai_evaluation.monitoring_lifecycle import lifecycle_decision

decision = lifecycle_decision(rule_results, drift_report)
```

This decision logic is illustrative. Real projects should add risk severity, incident history, label delay, subgroup findings, uncertainty, human oversight, and regulatory obligations.

## 8. Change control

Not every update requires the same amount of re-validation. A change-impact assessment should review:

```text
what changed
why it changed
affected system components
affected intended use
new hazards or failure modes
data and model compatibility
performance regression risk
monitoring impact
rollback plan
required testing and approval
```

Examples of changes include:

- retraining on new data;
- threshold modification;
- preprocessing update;
- feature addition or removal;
- model architecture change;
- dependency update;
- device or sensor change;
- user-interface change;
- new site or geography;
- expanded intended use.

## 9. Retraining triggers

Retraining should not be automatic merely because drift is detected. A trigger should be evidence-based and linked to root-cause analysis.

Possible triggers include:

- sustained performance below an action threshold;
- repeated subgroup degradation;
- confirmed distribution shift affecting validity;
- new classes or operating conditions;
- label-policy change;
- unacceptable calibration drift;
- repeated incidents or human overrides;
- major data or software change.

Before retraining, review data provenance, labels, representativeness, leakage, and whether retraining is the correct mitigation.

## 10. Re-validation after change

Re-validation should be proportionate to the change and risk. It may include:

- regression testing against the previous version;
- full dataset-quality review;
- overall and subgroup performance;
- robustness and stress testing;
- calibration and threshold review;
- external validation;
- human-factor evaluation;
- security and privacy review;
- updated monitoring thresholds;
- rollback verification.

A new version should not replace the approved version until acceptance criteria are met and the release decision is documented.

## 11. Incident and escalation management

A monitoring plan should define:

```text
signal owner
review frequency
warning response
action response
escalation route
incident severity
containment action
rollback authority
communication requirements
closure evidence
```

Possible containment actions include disabling a feature, switching to a fallback process, increasing human review, restricting the operating scope, or rolling back to a prior version.

## 12. Complete synthetic example

Run:

```bash
python examples/monitoring-and-lifecycle/monitoring_lifecycle_example.py
```

The example:

- creates 1,400 synthetic cases and six features;
- trains logistic regression;
- defines a reference window;
- simulates a changed current window;
- calculates reference and current metrics;
- applies warning and action thresholds;
- calculates feature drift using PSI;
- produces a lifecycle decision.

## 13. Monitoring report template

A useful report should contain:

```text
system and model version
monitoring period
reference baseline
sample and label counts
input-quality indicators
performance metrics
subgroup metrics
drift results
operational indicators
threshold status
incidents and overrides
root-cause investigation
mitigation or retraining action
lifecycle decision
owner and approval
next review date
```

## 14. Practical limitations

Monitoring data can be incomplete or delayed. Labels may arrive weeks or months after predictions. Drift metrics can flag harmless changes, and stable aggregate performance can hide local failures. For this reason, lifecycle decisions should combine quantitative signals, human review, operational context, uncertainty, and risk.

Monitoring is a continuous control process, not a one-time dashboard check.
