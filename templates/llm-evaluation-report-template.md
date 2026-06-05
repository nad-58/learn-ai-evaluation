# LLM Evaluation Report Template

This template supports public-safe technical evaluation of large language model applications. It should be adapted to the task, deployment context, risks, and evidence available.

## 1. Evaluation summary

**Project:**  
**Model and version:**  
**Evaluation date:**  
**Evaluator:**  
**Task type:** Question answering / summarisation / extraction / translation / dialogue / code / other  
**Evaluation status:** Exploratory / development / locked test / monitoring  

Summarise what was evaluated, the main findings, and the most important limitations.

## 2. Intended task

**Input:**  
**Expected output:**  
**User type:**  
**Human review:**  
**Reference answer available:** Yes / No / Sometimes  
**Grounding evidence available:** Yes / No  
**Required format:**  
**Out-of-scope uses:**  

## 3. Evaluation dataset

**Dataset version:**  
**Number of cases:**  
**Data source:** Synthetic / public / internal public-safe / other  
**Development-test separation:**  
**Languages:**  
**Domains:**  
**Difficulty bands:**  
**Input-length bands:**  
**Sensitive or high-risk cases included:**  
**Known coverage gaps:**  

## 4. Model and inference configuration

**Model identifier and version:**  
**System prompt version:**  
**Prompt-template version:**  
**Temperature:**  
**Top-p:**  
**Maximum output tokens:**  
**Seed or repeat policy:**  
**Tool, retrieval, or memory components:**  
**Software/library versions:**  

## 5. Automated metrics

| Metric | Value | Aggregation | Configuration | Interpretation and limitation |
|---|---:|---|---|---|
| Perplexity |  |  | Tokenizer/model/dataset |  |
| Exact match |  |  | Normalisation rules |  |
| Token precision |  |  | Tokenisation rules |  |
| Token recall |  |  | Tokenisation rules |  |
| Token F1 |  |  | Tokenisation rules |  |
| ROUGE-1 |  |  | Library/version |  |
| ROUGE-2 |  |  | Library/version |  |
| ROUGE-L |  |  | Library/version |  |
| BLEU |  |  | Tokenisation/smoothing |  |
| METEOR |  |  | Language resources |  |
| BERTScore |  |  | Embedding model/version |  |

## 6. LLM-as-a-judge evaluation

**Judge model and version:**  
**Judge prompt version:**  
**Rating scale:**  
**Temperature and repeat policy:**  
**Candidate order randomised:** Yes / No  
**Human agreement checked:** Yes / No  

| Criterion | Definition | Score | Acceptance target | Notes |
|---|---|---:|---:|---|
| Correctness |  |  |  |  |
| Completeness |  |  |  |  |
| Relevance |  |  |  |  |
| Clarity |  |  |  |  |
| Groundedness |  |  |  |  |
| Instruction following |  |  |  |  |
| Safety |  |  |  |  |

Describe controls for position bias, verbosity bias, self-preference, prompt sensitivity, and judge variability.

## 7. Human evaluation

**Number of evaluators:**  
**Evaluator expertise:**  
**Training/calibration performed:**  
**Blinded evaluation:** Yes / No  
**Cases evaluated by multiple reviewers:**  
**Agreement method:**  
**Disagreement-resolution method:**  

| Criterion | Rating scale | Mean/median | Agreement | Key observation |
|---|---|---:|---:|---|
| Correctness |  |  |  |  |
| Relevance |  |  |  |  |
| Completeness |  |  |  |  |
| Groundedness |  |  |  |  |
| Clarity |  |  |  |  |
| Safety |  |  |  |  |

## 8. Group performance

| Grouping | Group | Cases | Primary metric | Judge/human score | Failure rate | Limitation |
|---|---|---:|---:|---:|---:|---|
| Language |  |  |  |  |  |  |
| Topic/domain |  |  |  |  |  |  |
| Difficulty |  |  |  |  |  |  |
| Input length |  |  |  |  |  |  |
| Prompt style |  |  |  |  |  |  |

## 9. Robustness and stress testing

| Test condition | Expected behaviour | Observed behaviour | Metric change | Pass/concern | Notes |
|---|---|---|---:|---|---|
| Paraphrased prompt |  |  |  |  |  |
| Typographical errors |  |  |  |  |  |
| Long context |  |  |  |  |  |
| Conflicting instruction |  |  |  |  |  |
| Missing context |  |  |  |  |  |
| Adversarial request |  |  |  |  |  |

## 10. Failure analysis

| Failure type | Count | Example pattern | Possible cause | Impact | Follow-up action |
|---|---:|---|---|---|---|
| Incorrect answer |  |  |  |  |  |
| Unsupported claim |  |  |  |  |  |
| Incomplete answer |  |  |  |  |  |
| Format failure |  |  |  |  |  |
| Unsafe response |  |  |  |  |  |
| Refusal error |  |  |  |  |  |

## 11. Operational evaluation

| Measure | Result | Target | Notes |
|---|---:|---:|---|
| Median latency |  |  |  |
| Tail latency |  |  |  |
| Input tokens |  |  |  |
| Output tokens |  |  |  |
| Estimated cost per case |  |  |  |
| Timeout/failure rate |  |  |  |

## 12. Acceptance criteria

List pre-defined acceptance criteria and whether each was met. Avoid defining criteria after reviewing the final test results.

## 13. Traceability and reproducibility

Record dataset, prompt, model, code, configuration, metric library, judge, and report versions. State whether another evaluator could reproduce the results.

## 14. Limitations

State where the evaluation does not support a conclusion. Include small sample sizes, limited languages, weak references, judge bias, unavailable human review, and untested deployment conditions.

## 15. Conclusion

State what the evidence supports, what it does not support, and what evaluation should be added next.

## Public-safe checklist

- [ ] No confidential prompts, outputs, datasets, or client information are included.
- [ ] Model, prompt, dataset, and metric versions are recorded.
- [ ] Reference and normalisation rules are documented.
- [ ] Automated metrics are not treated as complete measures of quality.
- [ ] Judge and human rubrics are defined.
- [ ] Group results and failure cases are reviewed.
- [ ] Limitations and unsupported claims are clear.
