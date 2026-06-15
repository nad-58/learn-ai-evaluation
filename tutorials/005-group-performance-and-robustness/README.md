# Group Performance, Fairness, and Robustness Evaluation

Aggregate model performance can hide weak behaviour for a cohort, environment, device, site, data source, or operating condition. This tutorial explains how to evaluate group performance, fairness criteria, uncertainty, and robustness under controlled changes.

The detailed guide is here:

[`docs/fairness-and-robustness-detailed-guide.md`](../../docs/fairness-and-robustness-detailed-guide.md)

It is an original public-safe synthesis informed by the bias, robustness, and AI-testing materials supplied by the repository owner.

## Runnable examples

Run from the repository root:

```bash
python examples/group-performance-and-robustness/fairness_metrics_example.py
python examples/group-performance-and-robustness/group_robustness_example.py
```

Run the tests:

```bash
python -m pytest tests/test_fairness_metrics.py -q
python -m pytest tests/test_group_robustness.py -q
```

Reusable modules:

```text
src/learn_ai_evaluation/fairness_metrics.py
src/learn_ai_evaluation/group_robustness.py
```

## 1. Distinguish bias, fairness, and robustness

**Bias** is a systematic difference in data, model behaviour, or treatment. It can arise from human judgement, data collection, labels, sampling, engineering decisions, deployment conditions, and feedback loops.

**Fairness** concerns the effects of the system on people, groups, organisations, or society. Fairness is contextual and different fairness criteria may conflict.

**Robustness** concerns whether required properties remain acceptable when circumstances change, such as noise, missing inputs, device changes, distribution shift, unusual edge cases, or a new operating environment.

## 2. Sources of unwanted bias

Review three broad categories:

### Human and organisational sources

- historical decisions in labels;
- inconsistent annotation;
- cognitive bias;
- incomplete stakeholder analysis;
- policy or workflow choices;
- insufficient human oversight.

### Data sources

- representation and coverage;
- sampling and class imbalance;
- missingness by group;
- data accuracy and timeliness;
- label consistency;
- collection environment;
- proxy attributes;
- deployment drift.

### Engineering decisions

- feature selection and encoding;
- preprocessing;
- algorithm choice;
- objective and loss function;
- hyperparameter tuning;
- model capacity and interactions;
- calibration;
- threshold selection;
- missing-input handling.

## 3. Fairness metrics

The numerical example evaluates binary predictions using:

```text
selection rate = predicted positives / group size
true-positive rate = TP / (TP + FN)
false-positive rate = FP / (FP + TN)
positive predictive value = TP / (TP + FP)
```

### Demographic parity

Compare selection rates:

```text
parity ratio = comparison selection rate / reference selection rate
```

A ratio near `1` means similar positive-outcome rates, but this criterion does not account for differences in true prevalence.

### Equality of opportunity

Compare true-positive rates across groups. This focuses on whether genuinely positive cases are identified at similar rates.

### Predictive equality

Compare false-positive rates across groups. This focuses on whether genuinely negative cases are incorrectly assigned positive outcomes at similar rates.

### Equalized odds

Consider both true-positive-rate and false-positive-rate gaps:

```text
TPR gap = maximum group TPR - minimum group TPR
FPR gap = maximum group FPR - minimum group FPR
```

No single fairness metric is universally appropriate. Metric selection should follow intended use, affected stakeholders, plausible harms, and legal or ethical constraints.

## 4. Numerical fairness example

Run:

```bash
python examples/group-performance-and-robustness/fairness_metrics_example.py
```

The example uses 20 synthetic decisions, split evenly between groups A and B. It reports:

- confusion counts;
- selection rate;
- true-positive and false-positive rates;
- positive predictive value;
- demographic-parity ratio;
- equalized-odds gaps;
- best/worst gaps and ratios.

## 5. Group performance and uncertainty

For each group, report more than one metric:

- sample size and prevalence;
- precision;
- sensitivity or recall;
- specificity;
- F1;
- AUROC;
- AUPRC;
- Brier score;
- confidence intervals.

Separate four questions:

1. Does every group meet a standalone performance requirement?
2. Are between-group gaps acceptable?
3. Is the evidence statistically reliable?
4. Is the difference practically important?

For a metric where higher is better:

```text
absolute gap = best group - worst group
worst-to-best ratio = worst group / best group
```

A small gap is not reassuring if all groups perform poorly. A high overall score is not reassuring if one group performs poorly.

## 6. Robustness assessment workflow

A practical workflow is:

```text
1. Identify the property and operating condition.
2. Select metrics.
3. Define a baseline and acceptance threshold.
4. Select representative real or simulated test data.
5. Specify the protocol, severity, and random seed.
6. Execute the test.
7. Compare perturbed and baseline performance.
8. Investigate root causes.
9. Mitigate and retest.
10. Monitor after deployment.
```

A robustness claim should be narrow and testable. For example:

```text
The classifier retained accuracy above 0.90 on the specified cross-country traffic-sign test set, compared with a baseline of 0.95 and a maximum permitted drop of 0.05.
```

## 7. Statistical, formal, and empirical methods

### Statistical methods

Use datasets, metrics, uncertainty estimates, thresholds, and decision rules. Examples include bootstrap intervals, stress datasets, perturbation sweeps, and baseline comparisons.

### Formal methods

Seek mathematical guarantees over a defined domain using techniques such as model checking, abstract interpretation, or interval bounds. The claim is limited by the assumptions and verified domain.

### Empirical methods

Use experimentation, observation, expert review, scenario testing, and user studies. These are valuable when complete system behaviour cannot be represented mathematically.

The three approaches are complementary.

## 8. Robustness perturbations

The repository example tests:

- Gaussian noise;
- missing-input simulation;
- feature-scale shift.

Other domain-specific tests can include blur, compression, brightness variation, resolution reduction, sensor dropout, prompt variation, device or site change, prevalence shift, unusual combinations, temporal shift, and adversarial inputs.

Each scenario should record:

```text
rationale
affected inputs
severity
expected behaviour
random seed
baseline result
perturbed result
allowed degradation
decision
```

## 9. Complete synthetic example

Run:

```bash
python examples/group-performance-and-robustness/group_robustness_example.py
```

The example:

- generates 1,200 synthetic records with eight features;
- creates three operating-environment groups;
- introduces a controlled challenge in one group;
- trains logistic regression;
- reports per-group performance and bootstrap confidence intervals;
- calculates gaps and ratios;
- runs noise, missing-input, and scale-shift tests;
- applies illustrative acceptance criteria.

## 10. Acceptance criteria

Example only:

```yaml
minimum_worst_group_auroc: 0.75
maximum_auroc_gap: 0.12
minimum_group_size: 50
maximum_robustness_auroc_drop: 0.08
```

These are not universal recommendations. Criteria should be justified using intended use, risk, stakeholder needs, baseline evidence, and the consequences of false positives and false negatives.

A decision may be:

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

Define stakeholders, undesirable outcomes, sensitive and proxy attributes, testable requirements, and foreseeable changes in users, data, environment, policy, and societal norms.

### Design and development

Review representation, labels, features, algorithms, loss functions, thresholds, calibration, preprocessing, and engineering decisions.

### Verification and validation

Perform internal and external validity testing, subgroup evaluation, perturbation tests, proxy-feature analysis, uncertainty analysis, and independent-data evaluation where possible.

### Deployment and monitoring

Monitor group coverage, error rates, input and output drift, performance degradation, and changes to data, devices, users, policies, or intended use.

## 12. Mitigation and retesting

Potential actions include collecting targeted data, correcting labels, revising preprocessing, comparing algorithms, recalibrating, adjusting thresholds with documented trade-offs, adding input-quality controls, adding human review, restricting the operating scope, or retraining.

After mitigation, retest the affected groups and robustness scenarios and rerun the overall evaluation to detect regressions elsewhere.

## 13. Reporting checklist

Document:

- intended use and stakeholders;
- fairness concept and rationale;
- group definitions;
- data sources and coverage;
- sample and event counts;
- model version and threshold;
- per-group metrics and confidence intervals;
- gaps and ratios;
- perturbation scenarios and severities;
- baseline and perturbed results;
- acceptance criteria;
- failures, mitigations, and retest results;
- monitoring and change-control arrangements;
- limitations and residual risk.

Fairness and robustness evaluation is a continuous lifecycle activity, not a one-time test.
