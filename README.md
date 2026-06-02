# Learn AI Evaluation

A practical, code-first repository for learning how to evaluate AI and machine learning systems across the full AI lifecycle.

The repository starts with the foundations of classical machine learning evaluation and is now expanding into dataset evaluation, computer vision evaluation, medical AI evaluation, fairness, robustness, monitoring, LLM evaluation, VLM evaluation, RAG evaluation, and agentic AI evaluation.

## Why this repository exists

Many AI projects focus mainly on building models. However, a useful AI system requires more than model training. It requires clear evaluation of:

- the data used to train and test the system;
- the model behaviour under realistic conditions;
- the performance metrics selected for the task;
- robustness to noise, edge cases, and distribution shift;
- fairness and subgroup performance;
- system-level behaviour after integration or deployment;
- monitoring and re-evaluation over time.

The aim of this repository is to provide practical tutorials, notebooks, templates, and examples that make AI evaluation easier to understand and apply.

## Current focus

The current phase focuses on **Dataset Evaluation**:

1. Missing values
2. Duplicated records
3. Class imbalance and label distribution
4. Feature distribution
5. Categorical cardinality
6. Potential outliers
7. Data splitting and leakage
8. Dataset representativeness
9. Dataset documentation

New dataset-evaluation materials include:

```text
src/learn_ai_evaluation/dataset_quality.py
examples/dataset-evaluation/dataset_quality_example.py
templates/dataset-quality-report-template.md
tutorials/008-dataset-quality-evaluation/README.md
tutorials/009-data-splitting-and-leakage/README.md
```

Previous foundation topics include:

1. What is AI Evaluation?
2. Classification Metrics
3. Confusion Matrix and Threshold Selection
4. ROC-AUC and PR-AUC
5. Calibration and Confidence
6. Dataset Splitting and Leakage

## 7-day roadmap

The repository will grow step by step:

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

This repository is educational and technical. It avoids confidential case material and does not include client-specific documentation. Examples should use synthetic data, public datasets, or generalised scenarios.

## How to use

Clone the repository:

```bash
git clone https://github.com/nad-58/learn-ai-evaluation.git
cd learn-ai-evaluation
pip install -r requirements.txt
```

Run the dataset-evaluation example:

```bash
python examples/dataset-evaluation/dataset_quality_example.py
```

Then open any tutorial folder and run the related Python script or notebook.

## License

MIT License for code. Written educational material can be reused with attribution unless otherwise stated.
