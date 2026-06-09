# Automated Benchmarking and Regression Evaluation

Version 1.1.0 adds a repeatable benchmark and regression gate for the repository.

## Inputs

Benchmark cases:

```text
data/synthetic_benchmark.csv
```

Regression rules:

```text
data/benchmark_baseline.csv
```

Each rule defines:

- the reference baseline score;
- the absolute minimum acceptable score;
- the maximum permitted drop from the baseline.

The effective acceptance floor is the larger of:

```text
minimum_score
baseline_score - max_allowed_drop
```

## Run the benchmark

From the repository root:

```bash
python scripts/run_benchmark.py
```

Optional arguments:

```bash
python scripts/run_benchmark.py \
  --benchmark data/synthetic_benchmark.csv \
  --baseline data/benchmark_baseline.csv \
  --output-dir reports
```

## Outputs

The runner generates:

```text
reports/benchmark_results.json
reports/benchmark_results.csv
reports/benchmark_report.md
```

The JSON output is suitable for automation. The CSV output is suitable for analysis and dashboards. The Markdown output provides a readable summary.

## Regression behaviour

The command returns exit code `0` when every track passes. It returns exit code `1` when one or more tracks fall below the acceptance floor. This allows GitHub Actions to block a change that causes unacceptable degradation.

## Current tracks

- LLM
- VLM
- RAG
- Agentic AI
- Combined system-level evaluation
- Overall equal-weight aggregate

## Updating the baseline

Do not automatically replace the baseline after every run. A baseline update should be intentional and documented. Review the reason for the change, compare failure cases, confirm that the new score represents acceptable behaviour, and then update `data/benchmark_baseline.csv` in a separate reviewed commit.

## Limitations

The current benchmark is synthetic and small. It demonstrates regression-checking mechanics rather than production-level model validation. Real projects should use representative datasets, confidence intervals, subgroup analysis, repeated runs for stochastic systems, and risk-based acceptance criteria.
