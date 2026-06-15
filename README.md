# Learn AI Evaluation

A practical, code-first repository for evaluating AI and machine-learning systems across the lifecycle: data, models, groups, robustness, monitoring, and advanced AI systems.

## Quick navigation

| Goal | Start here |
|---|---|
| Evaluate data quality | [`tutorials/002-dataset-evaluation/README.md`](tutorials/002-dataset-evaluation/README.md) and [`dataset_quality_example.py`](examples/dataset-evaluation/dataset_quality_example.py) |
| Evaluate a computer-vision model | [`tutorials/003-computer-vision-evaluation/README.md`](tutorials/003-computer-vision-evaluation/README.md) and [`cv_metrics_example.py`](examples/computer-vision-evaluation/cv_metrics_example.py) |
| Review fairness and robustness | [`tutorials/005-group-performance-and-robustness/README.md`](tutorials/005-group-performance-and-robustness/README.md), [`docs/fairness-and-robustness-detailed-guide.md`](docs/fairness-and-robustness-detailed-guide.md), [`fairness_metrics_example.py`](examples/group-performance-and-robustness/fairness_metrics_example.py), and [`group_robustness_example.py`](examples/group-performance-and-robustness/group_robustness_example.py) |
| Review monitoring and lifecycle controls | Open the monitoring-and-lifecycle tutorial and example |
| Distinguish LLM, large vision model, VLM, and VLA | [`docs/llm-lvm-vlm-vla-taxonomy.md`](docs/llm-lvm-vlm-vla-taxonomy.md) |
| Evaluate a RAG system | [`tutorials/017-rag-evaluation/README.md`](tutorials/017-rag-evaluation/README.md) and [`basic_rag_evaluation_example.py`](examples/rag-evaluation/basic_rag_evaluation_example.py) |
| Run benchmark regression checks | [`docs/benchmark-regression-guide.md`](docs/benchmark-regression-guide.md) |
| Contribute | [`CONTRIBUTING.md`](CONTRIBUTING.md) |

## Dataset evaluation

```bash
python examples/dataset-evaluation/dataset_quality_example.py
python -m pytest tests/test_dataset_quality.py -q
```

Covers missingness, duplicates, class balance, feature distributions, categorical cardinality, outliers, split leakage, and reporting.

## Computer-vision evaluation

```bash
python examples/computer-vision-evaluation/classification_metrics_example.py
python examples/computer-vision-evaluation/segmentation_metrics_example.py
python examples/computer-vision-evaluation/detection_metrics_example.py
python examples/computer-vision-evaluation/cv_metrics_example.py
python -m pytest tests/test_computer_vision_metrics.py -q
```

Covers confusion matrices, per-class precision/recall/F1, pixel accuracy, IoU, Dice, bounding-box IoU, detection precision/recall, and average precision.

## Fairness and robustness evaluation

This track is an original public-safe synthesis informed by bias, robustness, and AI-testing materials supplied by the repository owner.

```text
tutorials/005-group-performance-and-robustness/README.md
docs/fairness-and-robustness-detailed-guide.md
src/learn_ai_evaluation/fairness_metrics.py
src/learn_ai_evaluation/group_robustness.py
examples/group-performance-and-robustness/fairness_metrics_example.py
examples/group-performance-and-robustness/group_robustness_example.py
tests/test_fairness_metrics.py
tests/test_group_robustness.py
```

Run the examples and tests:

```bash
python examples/group-performance-and-robustness/fairness_metrics_example.py
python examples/group-performance-and-robustness/group_robustness_example.py
python -m pytest tests/test_fairness_metrics.py -q
python -m pytest tests/test_group_robustness.py -q
```

Coverage includes:

- human, data, and engineering sources of unwanted bias;
- demographic parity and selection-rate ratios;
- equality of opportunity through true-positive-rate comparison;
- predictive equality through false-positive-rate comparison;
- equalized-odds gaps;
- positive predictive value and worst-group analysis;
- subgroup sample sizes, prevalence, confidence intervals, gaps, and ratios;
- statistical, formal, and empirical robustness approaches;
- Gaussian noise, missing-input, and feature-scale perturbations;
- baselines, thresholds, acceptance decisions, mitigation, and retesting;
- lifecycle monitoring, drift, and change control.

## Advanced evaluation

The repository also contains evaluation material for LLMs, large vision models, VLMs, RAG systems, VLA systems, agents, and combined systems.

```bash
python examples/advanced-ai-evaluation/advanced_ai_evaluation_example.py
python examples/llm-judge-evaluation/llm_judge_example.py
python examples/vlm-evaluation/basic_vlm_evaluation_example.py
python examples/rag-evaluation/basic_rag_evaluation_example.py
```

## Automated benchmark and regression checks

```bash
python scripts/run_benchmark.py
```

The runner compares current LLM, VLM, RAG, agent, and system-level scores with stored baselines and fails when a permitted regression limit is breached.

## Installation

```bash
git clone https://github.com/nad-58/learn-ai-evaluation.git
cd learn-ai-evaluation
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

## Full validation

```bash
python -m compileall -q src tests examples scripts
python -m pytest tests -q
python scripts/run_all_examples.py
python scripts/run_benchmark.py
python -m build
python -m twine check dist/*
```

## Public-safe scope

Examples use synthetic data, public datasets, or generalised scenarios. The repository does not include confidential client material.

## License

MIT License for code. Educational material can be reused with attribution unless otherwise stated.
