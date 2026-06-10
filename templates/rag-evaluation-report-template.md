# Retrieval-Augmented Generation Evaluation Report

## 1. Evaluation scope

- System identifier:
- Version:
- Evaluation date:
- Intended use:
- Query types:
- Important failure modes:

## 2. System configuration

- Corpus version:
- Chunking method:
- Embedding model:
- Index configuration:
- Retriever:
- Reranker:
- Top-K settings:
- Prompt template:
- Generator model and version:
- Decoding settings:

## 3. Evaluation dataset

- Number of queries:
- Answerable queries:
- Unanswerable queries:
- Relevance judgement method:
- Reference answer method:
- Source and licence:
- Dataset limitations:

## 4. Retrieval results

| Metric | Result | Target | Interpretation |
|---|---:|---:|---|
| Precision@K |  |  |  |
| Recall@K |  |  |  |
| MRR |  |  |  |
| MAP |  |  |  |

## 5. Context quality

| Dimension | Result | Method | Notes |
|---|---:|---|---|
| Context relevance |  |  |  |
| Evidence completeness |  |  |  |
| Duplicate context rate |  |  |  |
| Conflict rate |  |  |  |
| Truncation rate |  |  |  |

## 6. Answer quality

| Metric | Result | Target | Interpretation |
|---|---:|---:|---|
| Exact match |  |  |  |
| Token F1 |  |  |  |
| Human correctness score |  |  |  |
| Completeness score |  |  |  |

## 7. Faithfulness and grounding

- Claim decomposition method:
- Claim support rate:
- Unsupported claim rate:
- Contradiction rate:
- Overgeneralisation rate:
- Serious failures:

## 8. Citation quality

| Metric | Result | Target | Notes |
|---|---:|---:|---|
| Citation precision |  |  |  |
| Citation coverage |  |  |  |
| Broken citation rate |  |  |  |
| Misplaced citation rate |  |  |  |

## 9. Answerability and abstention

| Metric | Result | Target | Notes |
|---|---:|---:|---|
| Answerability accuracy |  |  |  |
| Appropriate abstention rate |  |  |  |
| Unnecessary abstention rate |  |  |  |
| Unsupported answer rate |  |  |  |

## 10. Group and slice analysis

| Slice | Samples | Retrieval result | Answer result | Grounding result | Action |
|---|---:|---:|---:|---:|---|
|  |  |  |  |  |  |

## 11. Robustness evaluation

| Test | Baseline | Perturbed | Performance drop | Notes |
|---|---:|---:|---:|---|
| Query paraphrase |  |  |  |  |
| Spelling variation |  |  |  |  |
| Distractor documents |  |  |  |  |
| Duplicate passages |  |  |  |  |
| Reordered context |  |  |  |  |
| Conflicting evidence |  |  |  |  |

## 12. Safety and security

- Retrieved prompt injection tests:
- Permission boundary tests:
- Sensitive data tests:
- Poisoned document tests:
- Citation spoofing tests:
- Residual risks:

## 13. Efficiency and operational behaviour

| Measure | Result | Test condition | Target |
|---|---:|---|---:|
| Retrieval latency |  |  |  |
| Generation latency |  |  |  |
| End-to-end latency |  |  |  |
| Context length |  |  |  |
| Token usage |  |  |  |
| Cost per query |  |  |  |
| Failure rate |  |  |  |

## 14. Failure analysis

| Failure ID | Query | Retrieval issue | Context issue | Answer issue | Severity | Action |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## 15. Reproducibility

- Code version:
- Corpus version:
- Evaluation dataset version:
- Metric implementation:
- Judge configuration:
- Software environment:
- Hardware:
- Random seed:
- Stored logs and artefacts:

## 16. Conclusions and re-evaluation triggers

- Main strengths:
- Main weaknesses:
- Unresolved limitations:
- Required mitigations:
- Re-evaluation triggers:
