# Vision-Language Model Evaluation Report

## 1. Evaluation information

- Model name:
- Model version or checkpoint:
- Evaluation date:
- Evaluator:
- Prompt template:
- Inference configuration:
- Answer extraction method:
- Dependency versions:

## 2. Evaluation scope

Select the capability groups included in this evaluation.

- Visual perception
- Visual knowledge acquisition
- Visual reasoning
- Visual commonsense
- Object hallucination
- Embodied or action-oriented planning
- Open-world or human preference evaluation

## 3. Dataset and task inventory

| Task ID | Capability group | Dataset or source | Task type | Number of samples | Metric |
|---|---|---|---|---:|---|
|  |  |  |  |  |  |

## 4. Prompt and output configuration

Document the prompt format and output-processing rules.

- System prompt:
- User prompt template:
- Multiple-choice answer format:
- Long-reasoning separation method:
- Final-answer extraction rule:
- Maximum output length:
- Prediction storage format:

## 5. Visual perception results

| Task | Accuracy | Object recall | Counting error | Notes |
|---|---:|---:|---:|---|
|  |  |  |  |  |

## 6. OCR and visual knowledge acquisition

| Task | Word accuracy | Entity F1 | Caption score | Semantic review | Notes |
|---|---:|---:|---:|---|---|
|  |  |  |  |  |  |

## 7. Visual reasoning and commonsense

| Task | Exact match | Token F1 | Accuracy | MRR | Human or judge score | Notes |
|---|---:|---:|---:|---:|---:|---|
|  |  |  |  |  |  |  |

## 8. Object hallucination review

Use balanced yes/no object-presence questions where possible.

| Dataset or split | Accuracy | Precision | Recall | F1 | Yes ratio | Unsupported-claim rate |
|---|---:|---:|---:|---:|---:|---:|
|  |  |  |  |  |  |  |

Review whether a high yes ratio indicates a tendency to claim that objects are present when they are not.

## 9. Embodied or planning evaluation

| Scenario | Object recognition | Spatial understanding | Conciseness | Reasonability | Executability | Notes |
|---|---:|---:|---:|---:|---:|---|
|  |  |  |  |  |  |  |

## 10. Open-world or pairwise evaluation

| Comparison ID | Model A | Model B | Preferred output | Tie | Both inadequate | Reason |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

Record whether model identities and answer order were hidden from reviewers.

## 11. Failure analysis

Classify observed failures.

- Missed object or scene
- Incorrect object count
- OCR error
- Key information extraction error
- Spatial reasoning error
- Commonsense error
- Unsupported visual claim
- Prompt-format failure
- Final-answer extraction failure
- Excessively long output
- Appropriate uncertainty or abstention
- Unnecessary abstention

## 12. Generalisation and reproducibility

Document:

- whether the evaluation is zero-shot or few-shot;
- whether any benchmark data may overlap with training data;
- whether results change across prompt templates;
- whether exact matching and semantic or judge-based extraction disagree;
- software and dependency versions;
- random seed and hardware where relevant;
- whether prediction files were checked for truncation.

## 13. Overall conclusion

Summarise strengths, limitations, important hallucination findings, generalisation concerns, and recommended improvements.

Decision:

Recommended next steps:
