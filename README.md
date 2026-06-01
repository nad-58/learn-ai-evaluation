# Learn AI Evaluation

A practical, code-first repository for learning how to evaluate AI and machine learning systems across the full AI lifecycle.

The repository starts with the foundations of classical machine learning evaluation and will gradually expand into dataset evaluation, computer vision evaluation, medical AI evaluation, fairness, robustness, monitoring, LLM evaluation, VLM evaluation, RAG evaluation, and agentic AI evaluation.

## Why this repository exists

Many AI projects focus mainly on building models. However, a useful AI system requires more than model training. It requires clear evaluation of:

- the data used to train and test the system;
- the model behaviour under realistic conditions;
- the performance metrics selected for the task;
- the performance metrics selected for the task;
- robustness to noise, edge cases, and distribution shift;
- fairness and subgroup performance;
- system-level behaviour after integration or deployment;
- monitoring and re-evaluation over time.

The aim of this repository is to provide practical tutorials, notebooks, templates, and examples that make AI evaluation easier to understand and apply.

## Current focus

The first version focuses on classical machine learning evaluation:

1. What is AI Evaluation?
2. Classification Metrics
3. Confusion Matrix and Threshold Selection
4. ROC-AUC and PR-AUC
5. Calibration and Confidence
6. Dataset Splitting and Leakage

## Future roadmap

The repository will grow step by step:

- Dataset Evaluation
- Classical ML Evaluation
- Computer Vision Evaluation
- Medical AI Evaluation
- Bias, Fairness, and Robustness
- Monitoring and Drift
- LLM Evaluation
- VLM Evaluation
- RAG Evaluation
- AI Agent and Agentic AI Evaluation

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

This repository is educational and technical. It avoids confidential case material and does not include client-specific documentation. Examples should use synthetic data, public datasets, or generalised scenarios.

## How to use

Clone the repository:

```bash
git clone https://github.com/nad-58/learn-ai-evaluation.git
cd learn-ai-evaluation
pip install -r requirements.txt
```

Then open any tutorial folder and run the related Python script or notebook.

## License

MIT License for code. Written educational material can be reused with attribution unless otherwise stated.
