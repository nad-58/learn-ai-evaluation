# Phase 7: Advanced AI Evaluation

This phase covers evaluation of modern AI systems that go beyond a single classical model. It focuses on five areas: large language models, vision language models, retrieval augmented generation, agentic AI, and combined system-level evaluation.

## 1. Large language model evaluation

LLM evaluation should not rely on one score. A useful review normally combines task quality, factual coverage, consistency, instruction following, uncertainty behaviour, and safety-related checks.

Common checks include:

- answer relevance;
- factual coverage;
- hallucination indicators;
- consistency across repeated prompts;
- refusal or uncertainty behaviour;
- instruction following;
- format compliance;
- human review for high-impact use cases.

Simple metrics in this repository include lexical overlap, required fact coverage, and refusal or uncertainty rate. These are educational metrics and should be supplemented with human review or stronger semantic evaluation for real projects.

## 2. Vision language model evaluation

Vision language models need both language and visual grounding evaluation. The model may produce fluent text while missing objects, inventing visual details, misreading text, or misunderstanding spatial relationships.

Common checks include:

- object or concept coverage;
- forbidden or hallucinated concepts;
- visual question answering quality;
- OCR and document understanding;
- counting;
- chart or table interpretation;
- spatial reasoning;
- consistency between answer and image content.

The example metric in this repository checks expected terms, forbidden terms, and a simple VLM answer score.

## 3. RAG evaluation

RAG systems should be evaluated as both a retrieval system and a generation system. A good answer is not enough if the wrong documents were retrieved, and good retrieval is not enough if the final answer is not grounded.

Common checks include:

- precision at k;
- recall at k;
- hit at k;
- context relevance;
- answer relevance;
- groundedness;
- citation coverage;
- faithfulness to retrieved context;
- behaviour when no good evidence exists.

The utilities include precision at k, recall at k, hit at k, groundedness score, and citation coverage.

## 4. Agentic AI evaluation

Agentic systems should be evaluated as multi-step workflows. The review should check whether the system chooses the right actions, uses tools correctly, recovers from errors, and completes the intended task.

Common checks include:

- action match rate;
- tool-use success;
- step success rate;
- end-to-end task success;
- planning quality;
- recovery from failed steps;
- traceability of decisions;
- human approval points where relevant.

The utilities include a simple `AgentStep` record and an `agent_trace_metrics` function.

## 5. Combined system-level evaluation

Many real systems combine multiple components. For example, a user prompt may pass through an LLM, a retriever, a document store, a tool call, an agent workflow, and a final answer generator.

System-level evaluation should therefore combine component scores with end-to-end evidence. It should consider:

- final answer quality;
- retrieval quality;
- grounding;
- tool reliability;
- agent trace quality;
- latency;
- cost;
- monitoring and update process;
- human oversight.

## Implementation in this repository

Core utilities:

```text
src/learn_ai_evaluation/advanced_ai.py
```

Worked example:

```bash
python examples/advanced-ai-evaluation/advanced_ai_evaluation_example.py
```

The example runs all five tracks: LLM, VLM, RAG, agentic AI, and combined system-level evaluation.

## Reporting guidance

For real projects, report both automated metrics and qualitative findings. Always describe the task, dataset, prompts, expected outputs, model version, retrieval settings, tool settings, evaluation criteria, limitations, and known failure modes.

## Limitations

The metrics here are intentionally lightweight and transparent. They are designed for learning and repository demonstrations. They should not be treated as complete evidence for production readiness without task-specific test sets, human review, stronger semantic metrics, and monitoring over time.
