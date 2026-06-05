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

The current phase focuses on **Technical Medical AI Evaluation**:

1. Case-level and subject-level evaluation units
2. Sensitivity, specificity, precision, negative predictive value, and balanced accuracy
3. Threshold selection and threshold sweeps
4. Confidence intervals and sample support
5. Calibration review
6. Multi-site and subgroup evaluation
7. Ground-truth quality and annotation uncertainty
8. Segmentation Dice and volume comparison
9. Split, leakage, and repeated-observation risks
10. Model update and re-evaluation principles
11. Public-safe technical reporting

New and existing medical-AI materials include:

```text
src/learn_ai_evaluation/medical_ai_evaluation.py
src/learn_ai_evaluation/medical_ai_metrics.py
examples/medical-ai-evaluation/medical_ai_binary_example.py
examples/medical-ai-evaluation/medical_ai_evaluation_example.py
templates/medical-ai-evaluation-report-template.md
tutorials/012-medical-ai-evaluation/README.md
```

Previous phases include:

1. Classical ML evaluation
2. Dataset evaluation, including missing values, duplicates, class imbalance, feature distribution, leakage checks, and dataset documentation
3. Computer vision evaluation, including classification, segmentation, object detection, split risks, and visual failure review

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

This repository is educational and technical. It avoids confidential case material and does not include client-specific documentation. Examples should use synthetic data, public datasets, or generalised scenarios. Medical-AI content addresses technical evaluation only and does not provide clinical advice or demonstrate suitability for clinical use.

## How to use

Clone the repository:

```bash
git clone https://github.com/nad-58/learn-ai-evaluation.git
cd learn-ai-evaluation
```

Run the current case-level medical AI example:

```bash
python examples/medical-ai-evaluation/medical_ai_evaluation_example.py
```

Run the threshold and calibration example:

```bash
python examples/medical-ai-evaluation/medical_ai_binary_example.py
```

You can also run earlier examples:

```bash
python examples/computer-vision-evaluation/cv_metrics_example.py
python examples/dataset-evaluation/dataset_quality_example.py
```

Then open any tutorial folder and run the related Python script or notebook.

## License

MIT License for code. Written educational material can be reused with attribution unless otherwise stated.