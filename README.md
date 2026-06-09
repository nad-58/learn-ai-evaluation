# Learn AI Evaluation

A practical, code-first repository for learning how to evaluate AI and machine learning systems across the full AI lifecycle.

The repository covers classical machine learning, dataset quality, computer vision, medical AI, group performance, robustness, lifecycle monitoring, and advanced AI evaluation including LLMs, large vision-language models, RAG systems, and AI agents.

## Quick navigation

| Goal | Start here |
|---|---|
| Understand the scope | Read this README and the roadmap |
| Evaluate data quality | Open the dataset-evaluation tutorial and example |
| Evaluate a computer vision model | Open the computer-vision tutorial and metrics example |
| Review fairness and robustness | Open the group-performance and robustness materials |
| Review monitoring and lifecycle controls | Open the monitoring-and-lifecycle tutorial and report template |
| Evaluate LLM, VLM, RAG, or agentic AI systems | Open the advanced-ai-evaluation tutorial, example, and templates |
| Review VLM/LVLM capability coverage and hallucination | Open [`docs/vlm-evaluation-notes.md`](docs/vlm-evaluation-notes.md) and [`templates/vlm-evaluation-report.md`](templates/vlm-evaluation-report.md) |
| Contribute | Read [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Cite the repository | Use [`CITATION.cff`](CITATION.cff) |

## Why this repository exists

Many AI projects focus mainly on building models. However, a useful AI system requires more than model training. It requires clear evaluation of data, model behaviour, metrics, robustness, fairness, system integration, monitoring, and re-evaluation over time.

The aim is to provide practical tutorials, templates, reusable Python utilities, and worked examples that make AI evaluation easier to understand and apply.

## Current focus

The current completed phase is **Advanced AI Evaluation**.

New materials include:

```text
src/learn_ai_evaluation/advanced_ai.py
examples/advanced-ai-evaluation/advanced_ai_evaluation_example.py
tutorials/007-advanced-ai-evaluation/README.md
templates/rag-evaluation-report.md
templates/agent-evaluation-report.md
templates/system-level-evaluation-report.md
tests/test_advanced_ai.py
```

The VLM evaluation track has also been expanded using lessons from LVLM-eHub and the open-source VLMEvalKit project:

```text
docs/vlm-evaluation-notes.md
src/learn_ai_evaluation/vlm_metrics.py
examples/vlm-evaluation/basic_vlm_evaluation_example.py
templates/vlm-evaluation-report.md
tests/test_vlm_metrics.py
```

The VLM materials cover six capability groups: visual perception, visual knowledge acquisition, visual reasoning, visual commonsense, object hallucination, and embodied or action-oriented intelligence. They also document generation-based evaluation, answer extraction, prompt-template effects, long-response handling, and human or pairwise review.

Run the worked examples:

```bash
python examples/advanced-ai-evaluation/advanced_ai_evaluation_example.py
python examples/vlm-evaluation/basic_vlm_evaluation_example.py
```

Run the Phase 7 and VLM tests:

```bash
python -m pytest tests/test_advanced_ai.py -q
python -m pytest tests/test_vlm_metrics.py -q
```

## Previous completed areas

- Classical ML evaluation
- Dataset evaluation, including missing values, duplicates, class imbalance, feature distributions, and leakage
- Computer vision evaluation, including classification, segmentation, detection, split risks, and failure review
- Technical medical AI evaluation, including case-level analysis, uncertainty, multi-site evaluation, robustness, change control, and lifecycle monitoring
- Group performance and robustness evaluation
- Monitoring and lifecycle evaluation
- Foundational large language model evaluation
- Large vision-language model evaluation

## 7-day roadmap

1. ✅ Classical ML Evaluation
2. ✅ Dataset Evaluation
3. ✅ Computer Vision Evaluation
4. ✅ Medical AI Evaluation
5. ✅ Group Performance and Robustness
6. ✅ Monitoring and Lifecycle Evaluation
7. ✅ Advanced AI Evaluation, including LLM, VLM, RAG, and agentic AI evaluation

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

## How to use

```bash
git clone https://github.com/nad-58/learn-ai-evaluation.git
cd learn-ai-evaluation
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Run examples from the repository root:

```bash
python examples/advanced-ai-evaluation/advanced_ai_evaluation_example.py
python examples/vlm-evaluation/basic_vlm_evaluation_example.py
python examples/monitoring-and-lifecycle/monitoring_lifecycle_example.py
python examples/group-performance-and-robustness/group_robustness_example.py
python examples/llm-evaluation/basic_llm_metrics_example.py
python examples/medical-ai-evaluation/medical_ai_evaluation_example.py
python examples/computer-vision-evaluation/cv_metrics_example.py
python examples/dataset-evaluation/dataset_quality_example.py
```

Run tests:

```bash
python -m pytest tests/ -q
```

Then open the related tutorial folder for interpretation, limitations, and reporting guidance.

## References used for the VLM track

- LVLM-eHub: a comprehensive benchmark combining quantitative evaluation and open-world human preference assessment.
- VLMEvalKit: an open-source toolkit using generation-based evaluation across many VLM models and benchmarks, with exact matching and LLM-based answer extraction.

These external resources are used as methodological references only. The examples and templates in this repository are simplified, original educational implementations.

## After exploring this repository

- For reusable lifecycle validation reports and templates, use the private **AI Model Validation Framework** repository.
- For architecture and layer-level system thinking, see [AI Architecture Stack](https://github.com/nad-58/ai-architecture-stack).
- For LLM/RAG groundedness, retrieval, traceability, and human oversight, see [LLM RAG Evaluation Governance](https://github.com/nad-58/llm-rag-evaluation-governance).
- For edge deployment and computer vision constraints, see [Edge AI Computer Vision Deployment](https://github.com/nad-58/edge-ai-computer-vision-deployment).

## Development and releases

- Contribution guidance: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Security policy: [`SECURITY.md`](SECURITY.md)
- Changelog: [`CHANGELOG.md`](CHANGELOG.md)
- Package metadata: [`pyproject.toml`](pyproject.toml)
- Citation metadata: [`CITATION.cff`](CITATION.cff)

## Public-safe scope

This repository is educational and technical. It avoids confidential case material and client-specific documentation. Examples use synthetic data, public datasets, or generalised scenarios.

## License

MIT License for code. Written educational material can be reused with attribution unless otherwise stated.
