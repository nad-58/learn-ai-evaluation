# Learn AI Evaluation

A practical, code-first repository for evaluating AI and machine-learning systems across the lifecycle: data, models, groups, robustness, monitoring, and advanced AI systems.

## Quick navigation

| Goal | Start here |
|---|---|
| Evaluate data quality | [`tutorials/002-dataset-evaluation/README.md`](tutorials/002-dataset-evaluation/README.md) and [`dataset_quality_example.py`](examples/dataset-evaluation/dataset_quality_example.py) |
| Evaluate a computer-vision model | [`tutorials/003-computer-vision-evaluation/README.md`](tutorials/003-computer-vision-evaluation/README.md) and [`cv_metrics_example.py`](examples/computer-vision-evaluation/cv_metrics_example.py) |
| Review fairness and robustness | [`tutorials/005-group-performance-and-robustness/README.md`](tutorials/005-group-performance-and-robustness/README.md), [`docs/fairness-and-robustness-detailed-guide.md`](docs/fairness-and-robustness-detailed-guide.md), [`fairness_metrics_example.py`](examples/group-performance-and-robustness/fairness_metrics_example.py), and [`group_robustness_example.py`](examples/group-performance-and-robustness/group_robustness_example.py) |
| Review monitoring and lifecycle controls | [`tutorials/006-monitoring-and-lifecycle/README.md`](tutorials/006-monitoring-and-lifecycle/README.md), [`docs/multimodal-monitoring-numerical-examples.md`](docs/multimodal-monitoring-numerical-examples.md), and [`multimodal_monitoring_example.py`](examples/monitoring-and-lifecycle/multimodal_monitoring_example.py) |
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

```bash
python examples/group-performance-and-robustness/fairness_metrics_example.py
python examples/group-performance-and-robustness/group_robustness_example.py
python -m pytest tests/test_fairness_metrics.py -q
python -m pytest tests/test_group_robustness.py -q
```

## Monitoring and lifecycle evaluation

Core monitoring files:

```text
tutorials/006-monitoring-and-lifecycle/README.md
src/learn_ai_evaluation/monitoring_lifecycle.py
examples/monitoring-and-lifecycle/threshold_example.py
examples/monitoring-and-lifecycle/drift_example.py
examples/monitoring-and-lifecycle/monitoring_lifecycle_example.py
tests/test_monitoring_lifecycle.py
```

Run the core examples:

```bash
python examples/monitoring-and-lifecycle/threshold_example.py
python examples/monitoring-and-lifecycle/drift_example.py
python examples/monitoring-and-lifecycle/monitoring_lifecycle_example.py
python -m pytest tests/test_monitoring_lifecycle.py -q
```

### Multimodal numerical monitoring

The repository includes explicit numerical datasets and code for tabular, image, and speech monitoring:

```text
docs/multimodal-monitoring-numerical-examples.md
src/learn_ai_evaluation/multimodal_monitoring.py
examples/monitoring-and-lifecycle/multimodal_monitoring_example.py
tests/test_multimodal_monitoring.py

data/monitoring/tabular_reference.csv
data/monitoring/tabular_current.csv
data/monitoring/image_reference.csv
data/monitoring/image_current.csv
data/monitoring/speech_reference.csv
data/monitoring/speech_current.csv
```

Run it:

```bash
python examples/monitoring-and-lifecycle/multimodal_monitoring_example.py
python -m pytest tests/test_multimodal_monitoring.py -q
```

It demonstrates:

- tabular drift using age, score, latency, and prediction data;
- image monitoring using 8 by 8 grayscale matrices;
- image brightness, contrast, bright-pixel, and edge statistics;
- speech monitoring using 32-sample synthetic waveforms;
- RMS amplitude, peak amplitude, zero-crossing rate, and dominant frequency;
- absolute and relative feature changes between reference and current windows.

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
