# Learn AI Evaluation

A practical, code-first repository for learning how to evaluate AI and machine learning systems across the full AI lifecycle.

The repository covers classical machine learning, dataset quality, computer vision, medical AI, group performance, robustness, lifecycle monitoring, and advanced AI evaluation including LLMs, large vision-language models, RAG systems, and AI agents.

## Why this repository exists

Many AI projects focus mainly on building models. However, a useful AI system requires more than model training. It requires clear evaluation of data, model behaviour, metrics, robustness, fairness, system integration, monitoring, and re-evaluation over time.

The aim is to provide practical tutorials, templates, reusable Python utilities, and worked examples that make AI evaluation easier to understand and apply.

## Current focus

The current completed phase is **Monitoring and Lifecycle Evaluation**.

New materials include:

```text
src/learn_ai_evaluation/monitoring_lifecycle.py
examples/monitoring-and-lifecycle/monitoring_lifecycle_example.py
tutorials/006-monitoring-and-lifecycle/README.md
templates/monitoring-lifecycle-report.md
tests/test_monitoring_lifecycle.py
```

Run the worked example:

```bash
python examples/monitoring-and-lifecycle/monitoring_lifecycle_example.py
```

Run the Phase 6 tests:

```bash
python -m pytest tests/test_monitoring_lifecycle.py -q
```

## Previous completed areas

- Classical ML evaluation
- Dataset evaluation, including missing values, duplicates, class imbalance, feature distributions, and leakage
- Computer vision evaluation, including classification, segmentation, detection, split risks, and failure review
- Technical medical AI evaluation, including case-level analysis, uncertainty, multi-site evaluation, robustness, change control, and lifecycle monitoring
- Group performance and robustness evaluation
- Foundational large language model evaluation
- Large vision-language model evaluation

## 7-day roadmap

1. ✅ Classical ML Evaluation
2. ✅ Dataset Evaluation
3. ✅ Computer Vision Evaluation
4. ✅ Medical AI Evaluation
5. ✅ Group Performance and Robustness
6. ✅ Monitoring and Lifecycle Evaluation
7. Advanced AI Evaluation, including LLM, VLM, RAG, and agentic AI evaluation

## Repository structure

```text
learn-ai-evaluation/
├── docs/                         # Roadmap, glossary, and conceptual notes
├── tutorials/                    # Main tutorial chapters
├── notebooks/                    # Runnable notebooks
├── src/learn_ai_evaluation/      # Reusable Python utilities
├── data/                         # Synthetic and public example datasets
├── templates/                    # Evaluation report and checklist templates
├── examples/                     # End-to-end worked examples
├── tests/                        # Lightweight automated checks
└── assets/                       # Figures and diagrams
```

## Public-safe scope

This repository is educational and technical. It avoids confidential case material and client-specific documentation. Examples use synthetic data, public datasets, or generalised scenarios.

## How to use

```bash
git clone https://github.com/nad-58/learn-ai-evaluation.git
cd learn-ai-evaluation
pip install -r requirements.txt
```

Run examples from the repository root:

```bash
python examples/monitoring-and-lifecycle/monitoring_lifecycle_example.py
python examples/group-performance-and-robustness/group_robustness_example.py
python examples/vlm-evaluation/basic_vlm_evaluation_example.py
python examples/llm-evaluation/basic_llm_metrics_example.py
python examples/medical-ai-evaluation/medical_ai_evaluation_example.py
python examples/computer-vision-evaluation/cv_metrics_example.py
python examples/dataset-evaluation/dataset_quality_example.py
```

Run tests:

```bash
python -m pytest tests/test_monitoring_lifecycle.py -q
python -m pytest tests/test_group_robustness.py -q
```

Then open the related tutorial folder for interpretation, limitations, and reporting guidance.

## License

MIT License for code. Written educational material can be reused with attribution unless otherwise stated.
