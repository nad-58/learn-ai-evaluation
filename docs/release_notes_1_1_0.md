# Learn AI Evaluation 1.1.0

Version 1.1.0 introduces automated benchmarking and regression evaluation.

## Added

- Automated benchmark runner: `scripts/run_benchmark.py`
- Reusable regression engine: `src/learn_ai_evaluation/benchmark_regression.py`
- Benchmark baseline and acceptance limits: `data/benchmark_baseline.csv`
- JSON, CSV, and Markdown benchmark reports under `reports/`
- Unit tests for benchmark loading, aggregation, and regression decisions
- GitHub Actions regression gate
- Benchmark report artifact upload from CI
- Benchmark regression guide

## Acceptance logic

For every track, the effective acceptance floor is the larger of:

```text
minimum_score
baseline_score - max_allowed_drop
```

A benchmark run fails when any current score is below its acceptance floor.

## Run locally

```bash
python scripts/run_benchmark.py
```

## Current benchmark tracks

- LLM
- VLM
- RAG
- Agentic AI
- Combined system-level evaluation
- Equal-weight overall score

## Important note

The benchmark data is synthetic and demonstrates regression-checking mechanics. Production projects should replace it with representative data and risk-based acceptance criteria.
