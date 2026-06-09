# Synthetic Advanced AI Benchmark

This public-safe educational dataset contains synthetic examples for prompt comparison, evaluator agreement, position-order checks, VLM hallucination, RAG grounding, agent task completion, and combined system evaluation.

## LLM prompt comparison

| Case | Baseline | Candidate | Human preference | Candidate first | Candidate second |
|---|---|---|---|---|---|
| LLM-01 | Monitoring checks performance. | Monitoring compares current behaviour with a baseline and detects drift. | Candidate | Candidate | Candidate |
| LLM-02 | Vibe checks are subjective. | Vibe checks are subjective, difficult to reproduce, and not scalable. | Candidate | Candidate | Candidate |
| LLM-03 | Groundedness means evidence support. | Groundedness is the degree to which an answer is supported by supplied evidence. | Tie | Candidate | Baseline |

## VLM cases

| Case | Question | Reference | Prediction | Unsupported claim |
|---|---|---|---|---|
| VLM-01 | What is shown on the dashboard? | Line chart, warning and metrics | Line chart, warning and metrics | No |
| VLM-02 | Is a bicycle visible? | No | Yes | Yes |
| VLM-03 | How many red objects are visible? | Two | Two | No |

## RAG cases

| Case | Relevant documents | Retrieved documents | Expected citation |
|---|---|---|---|
| RAG-01 | monitoring, risk | monitoring, dataset, risk | monitoring and risk |
| RAG-02 | retrieval_metrics | retrieval_metrics, monitoring, agents | retrieval_metrics |

## Agent cases

| Case | Expected steps | Actual steps | Step outcomes |
|---|---|---|---|
| AGENT-01 | search, read, summarise | search, read, summarise | pass, pass, pass |
| AGENT-02 | search, read, cite | search, answer, cite | pass, fail, fail |

## Combined system cases

| Case | LLM | VLM | RAG | Agent success | Latency ms | Cost USD |
|---|---:|---:|---:|---:|---:|---:|
| SYSTEM-01 | 0.90 | 0.85 | 0.88 | 1.0 | 920 | 0.012 |
| SYSTEM-02 | 0.78 | 0.70 | 0.62 | 0.0 | 1450 | 0.019 |
