# Fairness and Robustness Evaluation Guide

This guide expands the group-performance and robustness track with practical material on bias sources, fairness metrics, robustness methods, lifecycle controls, numerical examples, and acceptance decisions.

The content is an original public-safe synthesis informed by training materials previously supplied by the repository owner on bias, robustness, and AI testing. It does not reproduce proprietary course text or diagrams.

## 1. Bias, fairness, and robustness are different questions

**Bias** is a systematic difference in data, model behaviour, or treatment. Bias can arise from human decisions, data collection, labels, sampling, feature engineering, algorithm selection, hyperparameter choices, model structure, deployment conditions, and feedback loops.

**Fairness** concerns the effects of an AI system on people, groups, organisations, or society. It is contextual. A system can satisfy one fairness criterion while failing another, and universal fairness normally cannot be guaranteed.

**Robustness** concerns whether required properties remain acceptable when circumstances change. Relevant changes can include noise, missing inputs, image degradation, sensor dropout, device changes, data-source changes, shifts in prevalence, unusual edge cases, adversarial inputs, or a new operating environment.

These questions overlap but should not be collapsed into one metric.

## 2. Sources of unwanted bias

### Human and organisational sources

Examples include:

- historical decisions embedded in labels;
- inconsistent expert judgement;
- cognitive bias in annotation or review;
- policy choices that disadvantage a group;
- incomplete stakeholder analysis;
- inadequate human oversight.

### Data sources

Review:

- sampling and coverage;
- representativeness;
- class and subgroup imbalance;
- missingness by group;
- measurement quality;
- label accuracy and consistency;
- data provenance;
- timeliness;
- collection environment;
- proxy variables;
- drift after deployment.

### Engineering decisions

Potential sources include:

- feature selection and encoding;
- dimensionality reduction;
- preprocessing;
- algorithm family;
- objective and loss function;
- threshold selection;
- hyperparameter tuning;
- model capacity and interactions;
- calibration;
- missing-input handling;
- post-processing rules.

Bias assessment should therefore cover the lifecycle, not only final predictions.

## 3. Fairness metrics for binary classification

Assume a binary outcome with true label `Y`, predicted label `Y_hat`, and group attribute `A`.

### Selection rate

```text
selection rate = predicted positives / group size
```

It describes how often a group receives the positive outcome.

### Demographic parity

Demographic parity compares selection rates between groups.

```text
parity ratio = comparison-group selection rate / reference-group selection rate
```

A value close to `1` means similar selection rates. This metric does not account for differences in true outcome prevalence and may be inappropriate in some use cases.

### Equality of opportunity

Equality of opportunity compares true-positive rates:

```text
TPR = TP / (TP + FN)
```

It asks whether qualified or genuinely positive cases are identified at similar rates.

### Predictive equality

Predictive equality compares false-positive rates:

```text
FPR = FP / (FP + TN)
```

It asks whether genuinely negative cases are incorrectly assigned a positive outcome at similar rates.

### Equalized odds

Equalized odds considers both TPR and FPR. A practical assessment reports:

```text
TPR gap = maximum group TPR - minimum group TPR
FPR gap = maximum group FPR - minimum group FPR
```

### Predictive value parity

Compare positive predictive value:

```text
PPV = TP / (TP + FP)
```

This asks whether positive predictions have similar reliability across groups.

### Worst-group and gap reporting

For every selected metric, report:

```text
best group
worst group
absolute gap = best - worst
worst-to-best ratio = worst / best
sample size
prevalence
confidence interval
```

A small gap is not reassuring when every group performs poorly. A strong overall score is not reassuring when one group performs poorly.

## 4. Numerical fairness example

Run:

```bash
python examples/group-performance-and-robustness/fairness_metrics_example.py
```

The example contains 20 synthetic decisions, split evenly between groups A and B. It calculates:

- confusion counts;
- selection rate;
- true-positive rate;
- false-positive rate;
- positive predictive value;
- demographic-parity ratio;
- equalized-odds gaps;
- best/worst gaps and ratios.

Reusable functions:

```python
from learn_ai_evaluation.fairness_metrics import (
    group_confusion_rates,
    fairness_gap_summary,
    demographic_parity_ratio,
    equalized_odds_gaps,
)
```

## 5. Reliability of subgroup findings

Subgroup results should not be treated as reliable merely because a point estimate is available. Review:

- total group size;
- positive and negative event counts;
- class coverage;
- independence of observations;
- confidence intervals;
- repeated measurements from one person or source;
- multiplicity from testing many slices;
- practical rather than only statistical significance.

A group with a high AUROC but very few cases may require more evidence rather than a pass decision.

## 6. Robustness assessment workflow

A useful workflow is:

```text
1. Identify the system property and operating condition.
2. Define the metric or metrics.
3. Set a baseline and acceptance threshold.
4. Select representative robustness data or transformations.
5. Define the test protocol and random seed.
6. Execute the test.
7. Compare perturbed and baseline results.
8. Investigate failures and root causes.
9. Mitigate and retest.
10. Monitor the property after deployment.
```

A robustness claim should state exactly what was tested. For example:

```text
The classifier retained accuracy above 0.90 under the specified cross-country traffic-sign dataset, relative to a baseline accuracy of 0.95 and an allowed drop of 0.05.
```

This is narrower and more defensible than claiming that the model is generally robust.

## 7. Three complementary robustness approaches

### Statistical methods

Statistical methods evaluate performance using datasets and metrics. Important ingredients are:

- appropriate real or simulated test data;
- model and preprocessing configuration;
- task-appropriate metrics;
- uncertainty estimates;
- thresholds and a decision rule.

Examples include bootstrap confidence intervals, stress datasets, perturbation sweeps, worst-group performance, and comparison against a baseline.

### Formal methods

Formal methods seek mathematical guarantees over a defined domain. Examples include model checking, abstract interpretation, interval bounds, and proof that output cannot change beyond a limit for inputs inside a specified region.

Formal evidence can be powerful but is only as broad as the assumptions, model abstraction, and verified domain.

### Empirical methods

Empirical methods use experimentation, observation, expert review, scenario testing, and user studies. They are valuable when the complete system cannot be represented by a formal model or when real operational behaviour matters.

These approaches are complementary rather than mutually exclusive.

## 8. Robustness perturbations

The repository example covers:

```text
Gaussian noise
missing-input simulation
feature-scale shift
```

Other task-dependent tests can include:

- blur, compression, brightness and contrast changes;
- resolution reduction;
- sensor dropout;
- spelling and prompt variations;
- alternate devices or sites;
- unusual but plausible input combinations;
- prevalence shift;
- synthetic edge cases;
- adversarial examples;
- temporal and geographic shift.

Each scenario should record:

```text
name
rationale
affected inputs
severity
expected behaviour
random seed
baseline metric
perturbed metric
allowed degradation
decision
```

## 9. Run the complete group and robustness example

```bash
python examples/group-performance-and-robustness/group_robustness_example.py
```

The example:

- creates 1,200 synthetic cases and eight features;
- creates three operating-environment groups;
- introduces a controlled challenge in one group;
- trains a logistic-regression model;
- reports precision, sensitivity, specificity, F1, AUROC, AUPRC and Brier score;
- estimates bootstrap intervals;
- calculates group gaps and ratios;
- runs noise, missing-input and scale-shift tests;
- applies illustrative acceptance criteria.

## 10. Acceptance criteria

Criteria should be justified from intended use, harms, baseline evidence, stakeholder needs, and risk analysis. Example structure:

```yaml
minimum_worst_group_auroc: 0.75
maximum_auroc_gap: 0.12
minimum_group_size: 50
maximum_robustness_auroc_drop: 0.08
```

These values are examples, not universal recommendations.

A decision should distinguish:

```text
pass
pass with limitation
additional evidence required
mitigation and retest required
restricted use
fail
```

## 11. Lifecycle treatment

### Inception

- identify affected stakeholders;
- define undesirable outcomes;
- identify sensitive and proxy attributes;
- define testable fairness and robustness requirements;
- consider deployment changes, drift, evolving use cases, and social change.

### Design and development

- improve representation and coverage;
- review labels and annotation procedures;
- compare algorithms and features;
- evaluate threshold and calibration choices;
- maintain traceability of engineering decisions.

### Verification and validation

- perform internal and external validity testing;
- compare groups and operating conditions;
- investigate correlations with sensitive or proxy features;
- use independent datasets where possible;
- execute perturbation and stress tests;
- document uncertainty and limitations.

### Deployment and monitoring

- monitor input, output and performance drift;
- monitor group coverage and error rates;
- define investigation and escalation triggers;
- reassess after model, data, policy, user, device or environment changes;
- retest after mitigation or retraining.

## 12. Mitigation and retesting

Potential responses include:

- collect targeted data;
- correct labels;
- revise preprocessing;
- remove or carefully manage proxies;
- alter sampling or weighting;
- compare algorithms;
- recalibrate scores;
- adjust thresholds only with documented trade-off analysis;
- add input-quality controls;
- introduce human review;
- narrow the operating scope;
- retrain and rerun all affected tests.

Mitigation should be evaluated for side effects. Improving one metric or group can reduce performance elsewhere.

## 13. Reporting checklist

A complete report should document:

- intended use and affected stakeholders;
- fairness concept and rationale;
- group definitions and lawful/ethical basis;
- data sources and subgroup coverage;
- sample and event counts;
- thresholds and model version;
- per-group confusion rates and ranking metrics;
- confidence intervals;
- gap and ratio measures;
- robustness scenarios and severities;
- baseline and perturbed results;
- acceptance criteria;
- failures, mitigations and retest results;
- monitoring and change-control arrangements;
- limitations and residual risk.

Fairness and robustness evaluation is continuous. It should be repeated when data, users, environments, system components, policies, or intended use change.
