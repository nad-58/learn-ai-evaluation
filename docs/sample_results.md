# Sample Evaluation Results

These results are calculated from the synthetic examples in `data/synthetic_benchmark.md`.

## LLM

- First-order candidate win rate: 1.000
- Reversed-order candidate win rate: 0.667
- Order-adjusted win rate: 0.833
- Evaluator and human agreement: 0.667

## VLM

- Exact or concept-level success: 0.667
- Unsupported-claim rate: 0.333
- Counting accuracy: 1.000

## RAG

- Mean Precision at 3: 0.500
- Mean Recall at 3: 1.000
- Mean Hit at 3: 1.000
- Citation coverage: 1.000

## Agentic AI

- Mean action-match rate: 0.833
- Mean step-success rate: 0.667
- Task-success rate: 0.500

## Combined system

| Scenario | Composite | Latency ms | Estimated cost USD |
|---|---:|---:|---:|
| SYSTEM-01 | 0.908 | 920 | 0.012 |
| SYSTEM-02 | 0.525 | 1450 | 0.019 |
| Mean | 0.716 | 1185 | 0.0155 |

The examples show why evaluation should combine task quality, hallucination, retrieval, workflow success, latency, and cost.
