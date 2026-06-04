# 014 — Medical AI Test Data and Leakage

This chapter explains how to think about test data, data separation, and leakage in health-related AI evaluation. The content is public-safe and educational. It does not reproduce any confidential, draft, or official source material.

Data leakage occurs when information from the evaluation data influences model development, tuning, selection, or interpretation. Leakage can make performance look better than it really is. In medical AI, leakage can be subtle because one patient, subject, scan, encounter, site, or acquisition device may create multiple related samples.

## Why row-level random splitting can be unsafe

A simple random split treats every row as independent. This can be misleading when several rows come from the same patient or study. For example, if one patient has multiple images and some images are placed in training while other images are placed in testing, the test result may measure memorisation of patient-specific patterns rather than generalisation to new patients.

A safer evaluation usually defines an independence unit. Depending on the task, this may be:

- patient or subject;
- study or scan;
- encounter or episode;
- site or hospital;
- scanner or device;
- acquisition session;
- time period.

The selected unit should match the intended use and the main leakage risk.

## Common leakage sources

Leakage can happen through many routes:

- the same patient appears in both training and testing;
- near-duplicate images appear across splits;
- repeated scans are separated across splits;
- labels are influenced by model outputs;
- preprocessing is fitted on the full dataset before splitting;
- feature selection is performed before splitting;
- hyperparameters are tuned repeatedly on the test set;
- a test set is reused many times during development;
- site, scanner, or acquisition artefacts reveal the label;
- post-processing rules are adjusted after looking at test failures.

## Test data checklist

A test dataset should be described clearly enough for another reviewer to understand its relevance and limitations. Useful questions include:

- What is the source of the data?
- What is the intended population or operating setting?
- What are the inclusion and exclusion rules?
- What is the target label or reference source?
- What is the independence unit?
- Are duplicate and near-duplicate checks performed?
- Are repeated measurements handled consistently?
- Are subgroup counts documented?
- Are missing values and outliers documented?
- Is the test set separated from training, validation, tuning, and model selection?

## Validation approaches

Different validation approaches answer different questions.

A holdout split is simple and easy to communicate, but it can be unstable when the dataset is small or imbalanced.

K-fold cross-validation can help estimate performance during development, but it must be designed around the independence unit. Patient-level grouped cross-validation is usually safer than image-level cross-validation for patient data.

Stratified splitting can help preserve class balance or important subgroup proportions, but stratification does not remove leakage unless related samples are kept together.

Time-aware splitting is useful when the evaluation should simulate future data. For example, training on earlier data and testing on later data can reveal temporal drift.

External or site-separated testing can be useful when the target use environment includes data from different sources. It can reveal performance drops caused by site, scanner, protocol, workflow, or population differences.

## Practical split review

A useful split review should report:

- the number of samples in each split;
- the number of independent entities in each split;
- positive and negative counts in each split;
- subgroup counts in each split;
- overlap of entities between splits;
- whether preprocessing, feature selection, and tuning were performed inside the training process only;
- whether the final test set was used only for final evaluation.

## Python example

The repository includes a synthetic example showing why row-level splitting can produce patient overlap and how grouped splitting can reduce this leakage risk.

```bash
python examples/medical-ai-evaluation/patient_level_split_example.py
```

Related files:

```text
src/learn_ai_evaluation/medical_ai_splits.py
examples/medical-ai-evaluation/patient_level_split_example.py
templates/medical-ai-test-specification-template.md
```
