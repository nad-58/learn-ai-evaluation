# Retrieval-Augmented Generation Evaluation

Retrieval-augmented generation combines a retriever, a context-construction stage, and a language model. Evaluation must therefore separate retrieval quality from answer quality and then test the complete system end to end.

All examples in this chapter use synthetic, public-safe data.

## 1. Evaluation layers

A useful RAG evaluation plan covers four layers:

```text
Knowledge source and indexing
        ↓
Retrieval and ranking
        ↓
Context construction
        ↓
Answer generation and citation
```

A poor answer may result from missing source content, weak chunking, retrieval failure, irrelevant context, truncation, unsupported generation, or incorrect citations. A single answer score cannot identify these causes.

## 2. Build an evaluation record

For each query, record:

```text
query_id
query
expected_answerable
relevant_document_ids
retrieved_document_ids
retrieval_scores
context_passages
reference_answer
generated_answer
claims
citations
latency
review_notes
```

Keep a stable evaluation set and version the source corpus, chunking method, embedding model, retriever, reranker, prompt, and generator.

## 3. Retrieval metrics

### Precision@K

Precision@K measures how many of the top-K retrieved items are relevant:

```text
Precision@K = relevant items in top K / retrieved items in top K
```

High precision reduces irrelevant context, but it does not establish that all required evidence was found.

### Recall@K

Recall@K measures how much of the available relevant evidence was retrieved:

```text
Recall@K = relevant items in top K / all relevant items
```

Recall is especially important when several passages are needed to answer a query.

### Reciprocal rank and MRR

Reciprocal rank rewards systems that place the first relevant result near the top:

```text
RR = 1 / rank of first relevant result
MRR = mean reciprocal rank across queries
```

### Average precision

Average precision combines ranking quality across all relevant results. It averages precision at each rank where a relevant item appears.

Retrieval metrics require a documented relevance judgement. Report whether relevance is binary, graded, passage-level, document-level, or established by human review.

## 4. Context quality

Retrieval results may still be unsuitable after chunk selection and prompt construction. Evaluate:

- context relevance;
- evidence completeness;
- duplicated or conflicting passages;
- context ordering;
- truncation;
- source freshness;
- metadata accuracy;
- whether the context contains enough information to answer.

Distinguish retrieval failure from context-construction failure.

## 5. Answer correctness

For short factual answers, exact match or token F1 can be useful. For open-ended answers, use a structured rubric covering factual correctness, completeness, relevance, clarity, and appropriate uncertainty.

Do not rely only on lexical similarity. A response can be phrased differently and remain correct, or closely match a reference while introducing an unsupported claim.

## 6. Faithfulness and claim support

Break the generated response into claims and verify each claim against the retrieved context.

```text
Claim Support Rate
= claims supported by retrieved context / all generated claims
```

Useful failure categories include:

- unsupported claim;
- contradiction with context;
- overgeneralisation;
- incorrect synthesis across passages;
- stale or superseded evidence;
- answer based on prior model knowledge rather than supplied context.

Evaluate correctness against the source corpus separately from faithfulness to retrieved context. A faithful answer can still be wrong if the source is wrong, and a factually correct answer can still be ungrounded in the provided evidence.

## 7. Citation evaluation

Citation evaluation should check both citation correctness and citation completeness.

```text
Citation Precision
= citations that support their associated claims / all citations
```

```text
Citation Coverage
= supported claims with a valid citation / claims requiring citation
```

Also test broken references, incorrect document identifiers, citations attached to the wrong sentence, and citations to passages that mention a topic but do not support the claim.

## 8. Answerability and abstention

Include answerable and unanswerable queries. The system should answer when sufficient evidence is available and abstain or request clarification when it is not.

Measure:

- correct answer rate for answerable queries;
- appropriate abstention rate for unanswerable queries;
- unnecessary abstention rate;
- unsupported-answer rate;
- answerability decision accuracy.

Unanswerable examples may represent missing corpus coverage, ambiguous queries, contradictory evidence, access restrictions, or insufficiently recent information.

## 9. Robustness tests

Test controlled variations such as:

- query paraphrases;
- spelling errors and abbreviations;
- short and long queries;
- distractor documents;
- duplicate passages;
- document updates;
- chunk size and overlap changes;
- retrieval depth changes;
- reordered context;
- conflicting evidence;
- prompt injection within retrieved content.

Report both performance degradation and failure patterns.

## 10. Group and slice analysis

Evaluate by query type, source type, topic, language, answer length, number of required evidence passages, corpus age, retrieval difficulty, and answerability.

Always report sample counts with slice-level results. Aggregate averages can hide severe weaknesses in rare or complex queries.

## 11. Safety and security

RAG-specific tests should include:

- malicious instructions embedded in retrieved documents;
- data-access boundary failures;
- leakage of restricted content;
- unsafe source prioritisation;
- poisoned or manipulated documents;
- citation spoofing;
- retrieval of personal or sensitive information;
- failure to respect document-level permissions.

The model should treat retrieved content as evidence, not as trusted instructions.

## 12. Efficiency and operational evaluation

Record retrieval latency, generation latency, end-to-end latency, number of retrieved passages, context length, token usage, cost, cache behaviour, failed requests, and timeout rates.

Evaluate quality and efficiency together because increasing retrieval depth or context length may improve recall while increasing latency, cost, and irrelevant evidence.

## 13. Human and model-based judging

Use a clear rubric with separate dimensions for correctness, completeness, faithfulness, citation quality, relevance, and abstention. Validate model-based judges against human-reviewed examples and document the judge model, prompt, scoring scale, and agreement results.

## 14. End-to-end evaluation

An end-to-end test should verify that the complete system:

1. retrieves suitable evidence;
2. constructs usable context;
3. answers correctly;
4. grounds claims in the context;
5. cites evidence accurately;
6. abstains when evidence is insufficient;
7. meets latency and operational requirements.

Do not hide a retrieval failure behind a reasonable answer generated from model memory.

## 15. Reproducibility

Record the corpus version, chunking configuration, embedding model, index settings, retriever, reranker, top-K values, prompt template, generator version, decoding settings, metric implementation, judge configuration, software environment, and evaluation date.

Use `templates/rag-evaluation-report-template.md` for structured reporting.

## 16. Run the example

```bash
python examples/rag-evaluation/basic_rag_evaluation_example.py
```

The example demonstrates Precision@K, Recall@K, average precision, mean reciprocal rank, token F1, claim-support rate, citation precision, and answerability accuracy.

## Key lesson

RAG evaluation is not only answer evaluation. It must identify whether evidence exists, whether the right evidence was retrieved, whether the context preserved it, and whether the generated answer remained correct and grounded.
