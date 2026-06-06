# Learn AI Evaluation

A practical, code-first repository for learning how to evaluate AI and machine learning systems across the full AI lifecycle.

The repository covers classical machine learning, dataset quality, computer vision, medical AI, group performance, robustness, lifecycle monitoring, and advanced AI evaluation including LLMs, large vision-language models, RAG systems, and AI agents.

## Why this repository exists

Many AI projects focus mainly on building models. However, a useful AI system requires more than model training. It requires clear evaluation of:

- the data used to train and test the system;
- model behaviour under realistic conditions;
- the suitability and limitations of selected metrics;
- robustness to noise, edge cases, and distribution shift;
- fairness and group performance;
- system-level behaviour after integration or deployment;
- monitoring and re-evaluation over time.

The aim is to provide practical tutorials, templates, reusable Python utilities, and worked examples that make AI evaluation easier to understand and apply.

## Current focus

The current addition is **Large Vision-Language Model Evaluation**.

It covers:

1. Task-specific evaluation for visual question answering, captioning, retrieval, OCR, grounding, and multimodal reasoning
2. Separation of visual perception, cross-modal alignment, reasoning, and answer generation
3. Exact match and token-level F1
4. Retrieval Recall@K and mean reciprocal rank
5. Visual grounding and unsupported-claim analysis
6. Answerability and abstention evaluation
7. Group and slice performance analysis
8. Image and prompt robustness testing
9. Human and model-based judging
10. Safety and adversarial multimodal evaluation
11. Efficiency and operational behaviour
12. Integrated system-level evaluation
13. Reproducible reporting and failure analysis

The central principle is that a large vision-language model should not be judged only by fluent output or one benchmark score. Evaluation must establish whether responses are correct, visually grounded, robust, appropriately uncertain, safe, efficient, and reliable after integration.

New VLM materials include:

```text
src/learn_ai_evaluation/vlm_metrics.py
examples/vlm-evaluation/basic_vlm_evaluation_example.py
templates/vlm-evaluation-report-template.md
tutorials/016-large-vision-language-model-evaluation/README.md
```

Run the worked example:

```bash
python examples/vlm-evaluation/basic_vlm_evaluation_example.py
```

## Previous completed areas

- Classical ML evaluation
- Dataset evaluation, including missing values, duplicates, class imbalance, feature distributions, and leakage
- Computer vision evaluation, including classification, segmentation, detection, split risks, and failure review
- Technical medical AI evaluation, including case-level analysis, uncertainty, multi-site evaluation, robustness, change control, and lifecycle monitoring
- Foundational large language model evaluation

## 7-day roadmap

1. Classical ML Evaluation
2. Dataset Evaluation
3. Computer Vision Evaluation
4. Medical AI Evaluation
5. Group Performance and Robustness
6. Monitoring and Lifecycle Evaluation
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
└── assets/                       # Figures and diagrams
```

## Public-safe scope

This repository is educational and technical. It avoids confidential case material and client-specific documentation. Examples use synthetic data, public datasets, or generalised scenarios.

## How to use

```bash
git clone https://github.com/nad-58/learn-ai-evaluation.git
cd learn-ai-evaluation
```

Run examples from the repository root:

```bash
python examples/vlm-evaluation/basic_vlm_evaluation_example.py
python examples/llm-evaluation/basic_llm_metrics_example.py
python examples/medical-ai-evaluation/medical_ai_evaluation_example.py
python examples/computer-vision-evaluation/cv_metrics_example.py
python examples/dataset-evaluation/dataset_quality_example.py
```

Then open the related tutorial folder for equations, interpretation, limitations, and reporting guidance.

## License

MIT License for code. Written educational material can be reused with attribution unless otherwise stated.
