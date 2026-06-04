# 015 — Medical AI Change and Re-testing

This chapter explains how to evaluate changes to AI functions used in health-related software. It is public-safe and educational. It does not reproduce confidential, draft, or official source material.

AI evaluation is not a one-time activity. A model can change, the data can change, the software pipeline can change, and the deployment environment can change. Any of these changes can affect performance, calibration, robustness, subgroup behaviour, and user interpretation.

## Why change impact matters

A small software or data change can create a large evaluation impact. For example, a threshold change can alter sensitivity and specificity. A preprocessing change can alter model inputs. A library update can change numerical output. A new training dataset can change subgroup performance. A new post-processing rule can change the final output even when the model itself is unchanged.

For this reason, every change should be assessed before deciding whether no re-testing, partial re-testing, or full re-testing is appropriate.

## Common change types

Changes that should normally trigger an impact review include:

- model retraining;
- new or removed training data;
- label or reference update;
- architecture change;
- hyperparameter change;
- decision-threshold change;
- preprocessing change;
- post-processing change;
- calibration change;
- explainability method change;
- runtime environment change;
- library or dependency update;
- user-interface change;
- data source or acquisition protocol change;
- monitoring trigger or drift signal.

## Re-testing strategy

The re-testing strategy should be proportionate to the change and the risk. A full repeat of the evaluation may be needed when the model has been retrained, the architecture changed, the input distribution changed, or the output meaning changed.

Partial re-testing may be justified when the change is limited, well understood, and does not affect all functions or all operating conditions. The rationale should be documented clearly.

No re-testing should be used cautiously. It should be supported by a clear technical argument showing why the change cannot reasonably affect the evaluated behaviour.

## Back-to-back comparison

A useful re-testing method is to compare the previous model or pipeline with the changed model or pipeline on the same fixed evaluation dataset. This can reveal whether outputs changed, where they changed, and whether the changes are acceptable.

Back-to-back comparison can include:

- score difference distribution;
- changed binary decisions;
- changed segmentation masks;
- changed measurements;
- subgroup-specific changes;
- failure-case review of changed outputs.

The previous version should not be treated as automatically correct. It is a comparison point, not a perfect truth source.

## Continuous or adaptive behaviour

Some AI systems may be updated repeatedly or adapted over time. For public educational purposes, it is useful to distinguish between:

- a locked model, where the deployed model does not change automatically;
- a controlled update, where a new model version is released after review;
- a limited update, where only a restricted part of the model or threshold is updated;
- a targeted release, where a change applies only to a defined scope;
- an adaptive process, where the system can learn from new data under defined controls.

Adaptive behaviour requires strong control of data quality, annotation quality, release gates, monitoring signals, rollback plans, and re-testing triggers.

## Change-impact questions

A practical change review should ask:

- What changed?
- Why did it change?
- Which function is affected?
- Which input, output, or interface is affected?
- Does the change affect the model, data, threshold, pipeline, environment, or user workflow?
- Does the change affect the intended technical task?
- Does the change affect any subgroup differently?
- Does the change affect calibration?
- Does the change affect failure modes?
- What evidence supports the proposed level of re-testing?
- What is the rollback plan if the changed version performs worse?

## Related template

```text
templates/medical-ai-change-impact-checklist.md
```
