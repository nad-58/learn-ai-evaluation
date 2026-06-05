# 015 — Foundational LLM Evaluation

This tutorial introduces the first layer of large language model evaluation. It covers foundational automated metrics, model-based judging, and human evaluation. These methods should be combined because no single metric captures correctness, semantic quality, usefulness, safety, robustness, and operational performance at the same time.

## Learning objectives

After completing this tutorial, you should be able to:

- calculate and interpret perplexity, exact match, token-level F1, ROUGE, and BLEU;
- explain the purpose of METEOR and BERTScore;
- design an LLM-as-a-judge rubric;
- plan structured human evaluation;
- select metrics that match the task;
- recognise where each metric can produce misleading conclusions;
- build a multi-metric LLM evaluation matrix.

## 1. Start with the evaluation task

Before selecting metrics, define what the model is expected to do. Examples include question answering, summarisation, translation, extraction, classification, dialogue, report generation, code generation, or retrieval-augmented answering.

Record:

- the input and expected output;
- whether one correct answer or many valid answers are possible;
- whether a reference answer exists;
- which errors matter most;
- whether factual grounding is required;
- whether the output will be reviewed by a human;
- the expected language, format, length, tone, and safety constraints.

A metric is useful only when it measures something relevant to the task.

## 2. Perplexity

Perplexity measures how surprised a language model is by a token sequence. For token probabilities assigned by the model:

```text
PPL = exp[-(1/N) * sum(log P(x_i | x_1, ..., x_(i-1))))]
```

where `N` is the number of evaluated tokens and `P(x_i | context)` is the model probability assigned to the observed token.

**Interpretation:** lower is better. A lower value indicates that the model assigned higher probability to the observed sequence.

**Use it for:** evaluating next-token prediction on a fixed text corpus.

**Do not use it alone for:** factuality, instruction following, safety, usefulness, or comparison across models that use different tokenizers or evaluation preprocessing. Perplexity is most meaningful when the dataset, tokenizer, token handling, and calculation method are controlled.

## 3. Exact match

Exact match checks whether the generated answer is identical to the reference answer:

```text
EM = (1/N) * sum(I(prediction_i = reference_i))
```

where `I` is 1 when the prediction matches the reference and 0 otherwise.

**Interpretation:** higher is better.

**Use it for:** short-answer question answering, structured extraction, identifiers, dates, numbers, labels, and outputs with one expected form.

**Main limitation:** semantically correct alternatives receive a score of zero. For example, `forty-two` and `42` may communicate the same answer but fail strict exact match.

A normalisation policy may lowercase text, remove repeated whitespace, strip punctuation, or standardise number formats. The policy must be defined before evaluation because it changes the result.

## 4. Token-level precision, recall, and F1

Token-level F1 measures overlap between prediction and reference tokens.

```text
Precision = overlapping prediction tokens / prediction tokens
Recall    = overlapping reference tokens / reference tokens
F1        = 2 * Precision * Recall / (Precision + Recall)
```

**Interpretation:** higher is better.

**Use it for:** extractive question answering and short responses where partial overlap is meaningful.

**Main limitation:** token overlap does not guarantee semantic correctness. A response can repeat many reference words while changing the meaning. Tokenisation and text normalisation also influence the result.

## 5. ROUGE-N

ROUGE-N is commonly used for summarisation and measures recall-oriented n-gram overlap.

```text
ROUGE-N = overlapping reference n-grams / total reference n-grams
```

`ROUGE-1` evaluates unigram overlap, while `ROUGE-2` evaluates bigram overlap.

**Interpretation:** higher is better.

**Strength:** easy to calculate and useful for regression testing when reference summaries are available.

**Limitation:** it rewards lexical overlap and can undervalue valid paraphrases. It should not be treated as a complete measure of factual consistency or summary usefulness.

## 6. ROUGE-L

ROUGE-L uses the longest common subsequence between prediction and reference. It rewards shared token order without requiring every token to be adjacent.

A precision and recall can be calculated from the longest common subsequence length, followed by an F-measure:

```text
P_lcs = LCS(prediction, reference) / prediction length
R_lcs = LCS(prediction, reference) / reference length
ROUGE-L F1 = 2 * P_lcs * R_lcs / (P_lcs + R_lcs)
```

**Interpretation:** higher is better.

**Limitation:** it remains reference-dependent and lexical. It does not directly measure truthfulness.

## 7. BLEU

BLEU evaluates modified n-gram precision and applies a brevity penalty to discourage outputs that are too short.

```text
BLEU = BP * exp(sum(w_n * log(p_n)))
```

where `p_n` is clipped n-gram precision, `w_n` is the weight for each n-gram order, and `BP` is the brevity penalty.

A common brevity penalty is:

```text
BP = 1                         when candidate length > reference length
BP = exp(1 - reference/candidate) otherwise
```

**Interpretation:** higher is better, usually reported between 0 and 1 or multiplied by 100.

**Use it for:** corpus-level translation comparison and controlled generation tasks.

**Limitations:** sentence-level BLEU can be unstable, valid paraphrases may score poorly, and implementation details such as smoothing and tokenisation must be reported.

## 8. METEOR

METEOR aligns generated and reference words using exact matches and may also consider stems, synonyms, and word order. It combines unigram precision and recall with a penalty for fragmented matches.

A general form is:

```text
METEOR = weighted F-mean * (1 - fragmentation penalty)
```

**Interpretation:** higher is better.

**Strength:** more tolerant of some linguistic variation than strict n-gram overlap.

**Limitations:** results depend on language resources, tokenisation, stemming, synonym handling, and the implementation used.

## 9. BERTScore

BERTScore compares contextual token embeddings rather than requiring exact word overlap. Each token in one text is matched with a semantically similar token in the other text, and embedding similarity is aggregated into precision, recall, and F1-like scores.

A simplified similarity step is:

```text
similarity(i, j) = cosine(embedding(prediction_i), embedding(reference_j))
```

**Interpretation:** higher is better.

**Strength:** can recognise semantically similar paraphrases that lexical metrics miss.

**Limitations:** the score depends on the selected embedding model and version. High semantic similarity does not prove factual correctness, safety, or task completion.

## 10. LLM as a judge

An evaluator model can score outputs against a defined rubric. This is more general than naming one particular model and allows the judge model to be versioned and replaced.

A useful rubric may score each response from 1 to 5 for:

- correctness;
- completeness;
- relevance;
- clarity;
- faithfulness to supplied evidence;
- instruction following;
- safety.

The judge prompt should include the task, input, candidate output, reference or evidence where available, scoring definitions, and a required output format.

**Controls to include:**

- fixed judge model and version;
- fixed temperature and prompt;
- blinded candidate ordering;
- randomised answer position for pairwise comparison;
- repeated judging where variability matters;
- human review of a representative sample;
- agreement analysis between judge and humans;
- checks for verbosity, style, position, and self-preference bias.

An LLM judge is an evaluation instrument, not ground truth.

## 11. Human evaluation

Human evaluation is needed when quality depends on context, usefulness, factual reasoning, harm, specialist judgement, or multiple valid answers.

Use a written rubric with observable criteria. For example:

| Criterion | Question |
|---|---|
| Correctness | Are the claims accurate? |
| Relevance | Does the answer address the request? |
| Completeness | Are important parts missing? |
| Groundedness | Are claims supported by the provided evidence? |
| Clarity | Is the answer understandable and well organised? |
| Safety | Does it avoid unacceptable harmful behaviour? |

Good practice includes evaluator training, blinded review, multiple evaluators for a subset, disagreement resolution, and inter-rater agreement analysis. Human ratings should be accompanied by evaluator instructions and sample counts.

## 12. Metric-selection matrix

| Task | Useful starting metrics | Important additions |
|---|---|---|
| Short factual answer | Exact match, token F1 | semantic review, factuality |
| Extraction | Exact match, precision, recall, F1 | schema validity, field-level errors |
| Summarisation | ROUGE-1/2/L, BERTScore | factual consistency, coverage, human review |
| Translation | BLEU, METEOR, BERTScore | human adequacy and fluency |
| Open-ended assistant | LLM judge, human rubric | safety, robustness, subgroup testing |
| Grounded answer | Exact match where applicable, BERTScore | citation correctness, faithfulness, retrieval evaluation |
| Language modelling | Perplexity | downstream task and behavioural evaluation |

## 13. Why multiple metrics are required

The metrics measure different properties:

- perplexity measures token prediction;
- exact match measures strict equality;
- F1, ROUGE, and BLEU measure lexical overlap;
- METEOR adds linguistic matching;
- BERTScore measures embedding similarity;
- LLM judging applies a flexible rubric;
- human evaluation provides contextual judgement.

A strong evaluation combines complementary measures and reports disagreements between them. For example, a response may have low ROUGE but high human quality because it is a correct paraphrase. Another response may have high lexical overlap but contain a critical factual error.

## 14. Recommended evaluation workflow

1. Define the task, risks, and acceptance criteria.
2. Build a versioned evaluation dataset with representative cases.
3. Separate development examples from final evaluation examples.
4. Select task-appropriate automated metrics.
5. Add rubric-based judge and human evaluation where needed.
6. Test prompt variations, output formats, edge cases, and adversarial inputs.
7. Evaluate groups such as language, topic, difficulty, and input length.
8. Record model, prompt, inference settings, metric implementation, and dataset version.
9. Review individual failures instead of relying only on averages.
10. Repeat the evaluation after model, prompt, retrieval, tool, or system changes.

## 15. Important reporting details

Always report:

- model and model version;
- system prompt and prompt-template version;
- decoding settings;
- evaluation dataset version and sample count;
- reference-generation process;
- metric library and version;
- normalisation and tokenisation rules;
- aggregation method;
- confidence intervals or repeated-run variability where appropriate;
- subgroup results;
- judge prompt, model, and scale;
- human-evaluator instructions and agreement;
- limitations and known failure cases.

## Run the example

From the repository root:

```bash
python examples/llm-evaluation/basic_llm_metrics_example.py
```

The reusable educational implementation is located at:

```text
src/learn_ai_evaluation/llm_metrics.py
```

Use the report template at:

```text
templates/llm-evaluation-report-template.md
```

## Scope note

This is the foundation of the LLM evaluation section. Future additions can extend it with factuality, hallucination, toxicity, prompt robustness, multilingual performance, uncertainty, long-context evaluation, retrieval-augmented generation, tool use, latency, cost, privacy, security, and agentic workflow evaluation.