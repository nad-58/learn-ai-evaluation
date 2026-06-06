# Large Vision-Language Model Evaluation Report

## 1. Evaluation scope

- System or model identifier:
- Version or checkpoint:
- Evaluation date:
- Intended task:
- Intended users and environment:
- Unit of analysis:
- Important failure modes:

## 2. Model and system configuration

- Provider or runtime:
- Prompt template:
- System instructions:
- Decoding settings:
- Image preprocessing:
- Image resolution and order:
- Number of images per request:
- Retrieval, OCR, tools, or post-processing components:

## 3. Evaluation dataset

- Dataset name and version:
- Source and licence:
- Number of samples:
- Split method:
- Duplicate and leakage checks:
- Answerable and unanswerable sample counts:
- Capability coverage:
- Group and slice definitions:
- Known dataset limitations:

## 4. Metric definitions and acceptance criteria

| Dimension | Metric | Definition | Target or trigger | Rationale |
|---|---|---|---|---|
| Task correctness |  |  |  |  |
| Retrieval |  |  |  |  |
| Grounding |  |  |  |  |
| Unsupported claims |  |  |  |  |
| Abstention |  |  |  |  |
| Robustness |  |  |  |  |
| Safety |  |  |  |  |
| Efficiency |  |  |  |  |

## 5. Overall results

| Metric | Result | Confidence or variability | Interpretation |
|---|---:|---:|---|
| Exact match |  |  |  |
| Token F1 |  |  |  |
| Recall@K |  |  |  |
| Mean reciprocal rank |  |  |  |
| Unsupported claim rate |  |  |  |
| Appropriate abstention rate |  |  |  |
| Unnecessary abstention rate |  |  |  |

## 6. Capability results

| Capability | Samples | Metric | Result | Key failures |
|---|---:|---|---:|---|
| Object recognition |  |  |  |  |
| Counting |  |  |  |  |
| Spatial understanding |  |  |  |  |
| OCR and text reading |  |  |  |  |
| Charts and diagrams |  |  |  |  |
| Knowledge and reasoning |  |  |  |  |
| Multi-image understanding |  |  |  |  |

## 7. Grounding and hallucination review

- Claim review method:
- Reviewer instructions:
- Unsupported claim categories:
- Claim grounding precision:
- Output-level unsupported claim rate:
- Serious examples and mitigations:

## 8. Group and slice analysis

| Slice | Samples | Result | Reference result | Gap | Interpretation or action |
|---|---:|---:|---:|---:|---|
|  |  |  |  |  |  |

Document image quality, prompt type, task complexity, source, language, environment, and other relevant slices. Do not report a score without its sample count.

## 9. Robustness evaluation

| Test | Baseline | Perturbed | Relative drop | Expected answer preserved? | Action |
|---|---:|---:|---:|---|---|
| Blur |  |  |  |  |  |
| Compression |  |  |  |  |  |
| Brightness or contrast |  |  |  |  |  |
| Occlusion |  |  |  |  |  |
| Prompt paraphrase |  |  |  |  |  |
| Distractor text |  |  |  |  |  |

## 10. Human or judge-based evaluation

- Evaluation dimensions:
- Rating scale:
- Judge or reviewer details:
- Blinding and randomisation:
- Agreement checks:
- Conflict resolution:
- Known judge limitations:

## 11. Safety and adversarial testing

- Embedded-image instructions:
- Conflicting image and prompt instructions:
- Prompt injection:
- Privacy-sensitive content:
- Unsafe inference:
- Harmful completion rate:
- Benign over-refusal rate:
- Mitigations and residual risks:

## 12. Efficiency and operational evaluation

| Measure | Result | Test conditions | Target | Status |
|---|---:|---|---:|---|
| Latency |  |  |  |  |
| Throughput |  |  |  |  |
| Memory |  |  |  |  |
| Token usage |  |  |  |  |
| Cost per request |  |  |  |  |
| Failed request rate |  |  |  |  |

## 13. Integrated system evaluation

Describe preprocessing, OCR, retrieval, prompt construction, inference, tool use, post-processing, output parsing, user-interface behaviour, logging, fallback, monitoring, and human escalation.

## 14. Failure analysis

| Failure ID | Input condition | Expected behaviour | Observed behaviour | Root-cause hypothesis | Severity | Action |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## 15. Reproducibility record

- Code version or commit:
- Dataset version:
- Metric implementation:
- Software environment:
- Hardware:
- Random seed:
- Excluded or failed samples:
- Stored artefacts and logs:

## 16. Conclusions and limitations

- Main strengths:
- Main weaknesses:
- Unresolved risks:
- Conditions where results do not generalise:
- Required mitigations:
- Re-evaluation triggers:
