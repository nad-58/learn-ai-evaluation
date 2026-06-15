# Learn AI Evaluation

A practical, code-first repository for learning how to evaluate AI and machine learning systems across the full AI lifecycle.

The repository covers classical machine learning, dataset quality, computer vision, medical AI, group performance, robustness, lifecycle monitoring, and advanced AI evaluation including LLMs, large vision models, vision-language models, RAG systems, vision-language-action models, and AI agents.

## Quick navigation

| Goal | Start here |
|---|---|
| Understand the scope | Read this README and the roadmap |
| Distinguish LLM, large vision model, VLM, and VLA | Open [`docs/llm-lvm-vlm-vla-taxonomy.md`](docs/llm-lvm-vlm-vla-taxonomy.md) |
| Evaluate data quality | Open [`tutorials/002-dataset-evaluation/README.md`](tutorials/002-dataset-evaluation/README.md) and run [`examples/dataset-evaluation/dataset_quality_example.py`](examples/dataset-evaluation/dataset_quality_example.py) |
| Evaluate a computer vision model | Open [`tutorials/003-computer-vision-evaluation/README.md`](tutorials/003-computer-vision-evaluation/README.md) and run [`examples/computer-vision-evaluation/cv_metrics_example.py`](examples/computer-vision-evaluation/cv_metrics_example.py) |
| Review fairness and robustness | Open the group-performance and robustness materials |
| Review monitoring and lifecycle controls | Open the monitoring-and-lifecycle tutorial and report template |
| Evaluate LLM, VLM, RAG, VLA, or agentic AI systems | Open the advanced-ai-evaluation tutorials, examples, and templates |
| Move beyond manual prompt checking | Open [`systematic-llm-evaluation.md`](tutorials/007-advanced-ai-evaluation/systematic-llm-evaluation.md) |
| Review VLM capability coverage and hallucination | Open [`tutorials/016-large-vision-language-model-evaluation/README.md`](tutorials/016-large-vision-language-model-evaluation/README.md) |
| Evaluate a RAG system | Open [`tutorials/017-rag-evaluation/README.md`](tutorials/017-rag-evaluation/README.md), [`examples/rag-evaluation/basic_rag_evaluation_example.py`](examples/rag-evaluation/basic_rag_evaluation_example.py), and [`templates/rag-evaluation-report-template.md`](templates/rag-evaluation-report-template.md) |
| Run automated benchmark regression checks | Open [`docs/benchmark-regression-guide.md`](docs/benchmark-regression-guide.md) |
| Review benchmark thresholds | Open [`data/benchmark_baseline.csv`](data/benchmark_baseline.csv) |
| Review generated benchmark results | Open [`reports/benchmark_report.md`](reports/benchmark_report.md) |
| Review v1.1.0 release notes | Open [`docs/release_notes_1_1_0.md`](docs/release_notes_1_1_0.md) |
| Contribute | Read [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Cite the repository | Use [`CITATION.cff`](CITATION.cff) |

## Why this repository exists

Many AI projects focus mainly on building models. A useful AI system requires more than model training. It requires clear evaluation of data, model behaviour, metrics, robustness, fairness, system integration, monitoring, and re-evaluation over time.

The aim is to provide practical tutorials, templates, reusable Python utilities, benchmarks, and worked examples that make AI evaluation easier to understand and apply.

## Dataset evaluation

The dataset-evaluation track contains:

```text
tutorials/002-dataset-evaluation/README.md
src/learn_ai_evaluation/dataset_quality.py
examples/dataset-evaluation/dataset_quality_example.py
tests/test_dataset_quality.py
```

Run the example:

```bash
python examples/dataset-evaluation/dataset_quality_example.py
```

Run the tests:

```bash
python -m pytest tests/test_dataset_quality.py -q
```

The track covers missing values, duplicates, class balance, numeric feature distributions, categorical cardinality, potential outliers, exact split overlap, and generated Markdown reporting.

## Computer vision evaluation

The computer-vision track contains:

```text
tutorials/003-computer-vision-evaluation/README.md
src/learn_ai_evaluation/computer_vision_metrics.py
examples/computer-vision-evaluation/classification_metrics_example.py
examples/computer-vision-evaluation/segmentation_metrics_example.py
examples/computer-vision-evaluation/detection_metrics_example.py
examples/computer-vision-evaluation/cv_metrics_example.py
tests/test_computer_vision_metrics.py
```

Run the combined example:

```bash
python examples/computer-vision-evaluation/cv_metrics_example.py
```

Run the individual examples:

```bash
python examples/computer-vision-evaluation/classification_metrics_example.py
python examples/computer-vision-evaluation/segmentation_metrics_example.py
python examples/computer-vision-evaluation/detection_metrics_example.py
```

Run the tests:

```bash
python -m pytest tests/test_computer_vision_metrics.py -q
```

The track covers classification confusion matrices, per-class precision, recall and F1, binary and multiclass segmentation, pixel accuracy, IoU, Dice, bounding-box overlap, detection precision and recall, and average precision.

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

Run automated benchmarking:

```bash
python scripts/run_benchmark.py
```

For each track, the effective acceptance floor is:

```text
max(minimum_score, baseline_score - max_allowed_drop)
```

The command fails when any track falls below this floor. GitHub Actions uses this behaviour as a regression gate and uploads the generated reports as a workflow artifact.

## Advanced evaluation resources

The model-family taxonomy includes:

```text
docs/llm-lvm-vlm-vla-taxonomy.md
```

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

The RAG evaluation track includes:

```text
src/learn_ai_evaluation/rag_metrics.py
examples/rag-evaluation/basic_rag_evaluation_example.py
tutorials/017-rag-evaluation/README.md
templates/rag-evaluation-report-template.md
tests/test_rag_metrics.py
```

## Completed roadmap

1. ✅ Classical ML Evaluation
2. ✅ Dataset Evaluation
3. ✅ Computer Vision Evaluation
4. ✅ Medical AI Evaluation
5. ✅ Group Performance and Robustness
6. ✅ Monitoring and Lifecycle Evaluation
7. ✅ Advanced AI Evaluation, including LLM, large vision model, VLM, RAG, VLA, and agentic AI evaluation
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

```bash
python -m compileall -q src tests examples scripts
python -m pytest tests -q
python scripts/run_all_examples.py
python scripts/run_benchmark.py
python -m build
python -m twine check dist/*
```

GitHub Actions performs the same checks for pushes and pull requests.

## Public-safe scope

This repository is educational and technical. It avoids confidential case material and client-specific documentation. Examples use synthetic data, public datasets, or generalised scenarios.

## License

MIT License for code. Written educational material can be reused with attribution unless otherwise stated.
