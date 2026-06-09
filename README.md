# Learn AI Evaluation

A practical, code-first repository for learning how to evaluate AI and machine learning systems across the full AI lifecycle.

The repository covers classical machine learning, dataset quality, computer vision, medical AI, group performance, robustness, lifecycle monitoring, and advanced AI evaluation including LLMs, vision-language models, RAG systems, and AI agents.

## Quick navigation

| Goal | Start here |
|---|---|
| Understand the scope | Read this README and the roadmap |
| Evaluate data quality | Open the dataset-evaluation tutorial and example |
| Evaluate a computer vision model | Open the computer-vision tutorial and metrics example |
| Review fairness and robustness | Open the group-performance and robustness materials |
| Review monitoring and lifecycle controls | Open the monitoring-and-lifecycle tutorial and report template |
| Evaluate LLM, VLM, RAG, or agentic AI systems | Open the advanced-ai-evaluation tutorial, example, and templates |
| Move beyond manual prompt checking | Open [`systematic-llm-evaluation.md`](tutorials/007-advanced-ai-evaluation/systematic-llm-evaluation.md) |
| Review VLM capability coverage and hallucination | Open [`docs/vlm-evaluation-notes.md`](docs/vlm-evaluation-notes.md) and [`templates/vlm-evaluation-report.md`](templates/vlm-evaluation-report.md) |
| Run automated benchmark regression checks | Open [`docs/benchmark-regression-guide.md`](docs/benchmark-regression-guide.md) |
| Review benchmark thresholds | Open [`data/benchmark_baseline.csv`](data/benchmark_baseline.csv) |
| Review generated benchmark results | Open [`reports/benchmark_report.md`](reports/benchmark_report.md) |
| Review v1.1.0 release notes | Open [`docs/release_notes_1_1_0.md`](docs/release_notes_1_1_0.md) |
| Contribute | Read [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Cite the repository | Use [`CITATION.cff`](CITATION.cff) |

## Why this repository exists

Many AI projects focus mainly on building models. A useful AI system requires more than model training. It requires clear evaluation of data, model behaviour, metrics, robustness, fairness, system integration, monitoring, and re-evaluation over time.

The aim is to provide practical tutorials, templates, reusable Python utilities, benchmarks, and worked examples that make AI evaluation easier to understand and apply.

## Current release

The current package version is **1.1.0 — Automated Benchmarking and Regression Evaluation**.

Version 1.1.0 adds:

```text
src/learn_ai_evaluation/benchmark_regression.py
scripts/run_benchmark.py
data/benchmark_baseline.csv
reports/benchmark_results.json
reports/benchmark_results.csv
reports/benchmark_report.md
tests/test_benchmark_regression.py
docs/benchmark-regression-guide.md
```

The benchmark runner reads the synthetic benchmark, calculates per-track and overall scores, compares them with acceptance rules, generates three report formats, and returns a non-zero exit code when a regression is detected.

## Run automated benchmarking

From the repository root:

```bash
python scripts/run_benchmark.py
```

Generated outputs:

```text
reports/benchmark_results.json
reports/benchmark_results.csv
reports/benchmark_report.md
```

Optional configuration:

```bash
python scripts/run_benchmark.py \
  --benchmark data/synthetic_benchmark.csv \
  --baseline data/benchmark_baseline.csv \
  --output-dir reports
```

For each track, the effective acceptance floor is:

```text
max(minimum_score, baseline_score - max_allowed_drop)
```

The command fails when any track falls below this floor. GitHub Actions uses this behaviour as a regression gate and uploads the generated reports as a workflow artifact.

## Advanced evaluation resources

The systematic LLM evaluation track includes:

```text
src/learn_ai_evaluation/llm_judge.py
tutorials/007-advanced-ai-evaluation/systematic-llm-evaluation.md
examples/llm-judge-evaluation/llm_judge_example.py
templates/llm-evaluation-playbook.md
templates/llm-evaluator-alignment.md
templates/prompt-iteration-report.md
tests/test_llm_judge.py
```

The VLM evaluation track includes:

```text
docs/vlm-evaluation-notes.md
src/learn_ai_evaluation/vlm_metrics.py
examples/vlm-evaluation/basic_vlm_evaluation_example.py
templates/vlm-evaluation-report.md
tests/test_vlm_metrics.py
```

The broader advanced evaluation phase includes LLM, VLM, RAG, agentic AI, and combined system-level evaluation.

## Completed roadmap

1. ✅ Classical ML Evaluation
2. ✅ Dataset Evaluation
3. ✅ Computer Vision Evaluation
4. ✅ Medical AI Evaluation
5. ✅ Group Performance and Robustness
6. ✅ Monitoring and Lifecycle Evaluation
7. ✅ Advanced AI Evaluation, including LLM, VLM, RAG, and agentic AI evaluation
8. ✅ Automated Benchmarking and Regression Evaluation

## Repository structure

```text
learn-ai-evaluation/
├── docs/                         # Roadmap, guides, reports, and conceptual notes
├── tutorials/                    # Main tutorial chapters
├── notebooks/                    # Runnable notebooks
├── src/learn_ai_evaluation/      # Reusable Python utilities
├── data/                         # Synthetic benchmark data and baselines
├── reports/                      # Machine-readable and human-readable results
├── templates/                    # Evaluation report and checklist templates
├── examples/                     # End-to-end worked examples
├── scripts/                      # Validation and benchmark runners
├── tests/                        # Automated checks
└── assets/                       # Figures and diagrams
```

## Installation

```bash
git clone https://github.com/nad-58/learn-ai-evaluation.git
cd learn-ai-evaluation
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

## Validation

Run the full local validation sequence:

```bash
python -m compileall -q src tests examples scripts
python -m pytest tests -q
python scripts/run_all_examples.py
python scripts/run_benchmark.py
python -m build
python -m twine check dist/*
```

GitHub Actions performs the same checks for pushes and pull requests. Benchmark reports are uploaded as CI artifacts.

## Methodological references used in the advanced tracks

The systematic LLM evaluation track was informed by the provided engineering playbook on moving beyond subjective output review toward measurable, repeatable prompt evaluation. The repository implementation uses original educational utilities and templates.

For the VLM track:

- LVLM-eHub provides a benchmark structure combining quantitative evaluation and open-world human preference assessment.
- VLMEvalKit provides an open-source reference for generation-based evaluation across many VLM models and benchmarks, with exact matching and model-based answer extraction.

## Development and releases

- v1.1.0 notes: [`docs/release_notes_1_1_0.md`](docs/release_notes_1_1_0.md)
- v1.0.0 notes: [`docs/release_notes_1_0_0.md`](docs/release_notes_1_0_0.md)
- Contribution guidance: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Security policy: [`SECURITY.md`](SECURITY.md)
- Changelog: [`CHANGELOG.md`](CHANGELOG.md)
- Package metadata: [`pyproject.toml`](pyproject.toml)
- Citation metadata: [`CITATION.cff`](CITATION.cff)

## Public-safe scope

This repository is educational and technical. It avoids confidential case material and client-specific documentation. Examples use synthetic data, public datasets, or generalised scenarios.

## License

MIT License for code. Written educational material can be reused with attribution unless otherwise stated.
