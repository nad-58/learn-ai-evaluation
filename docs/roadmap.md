# Roadmap

This repository follows a seven-phase learning roadmap from foundational machine-learning evaluation to advanced multimodal and agentic AI evaluation.

## Current tutorials

- 001 What is AI Evaluation?
- 002 Classification Metrics
- 003 Group Performance Evaluation
- 004 Robustness Evaluation
- 008 Dataset Quality Evaluation
- 009 Data Splitting and Leakage
- 010 Computer Vision Evaluation
- 011 Computer Vision Dataset Splits and Failure Review
- 015 Foundational Large Language Model Evaluation
- 016 Large Vision-Language Model Evaluation
- 017 Retrieval-Augmented Generation Evaluation

## Phase 1 — Foundations and Classical ML Evaluation

- What is AI Evaluation?
- Classification metrics
- Group performance evaluation
- Robustness evaluation
- Confusion matrix and threshold selection
- ROC-AUC and PR-AUC
- Calibration and confidence
- Dataset splitting and leakage
- Cross-validation
- Error analysis
- Class imbalance

## Phase 2 — Dataset Evaluation

- Dataset quality assessment
- Missing data and duplicates
- Label quality
- Annotation agreement
- Train, validation, and test splitting
- Data leakage
- Data distribution analysis
- Dataset documentation

## Phase 3 — Computer Vision Evaluation

- Image classification metrics
- Confusion matrices and per-class precision, recall, and F1
- Object detection IoU, precision, recall, and average precision
- Segmentation IoU, Dice, and pixel accuracy
- Image quality and preprocessing impact
- Dataset split risks for images, video frames, scenes, subjects, and objects
- Visual failure-case review
- Input variation and robustness testing
- Public-safe computer vision evaluation reporting

## Phase 4 — Medical AI Evaluation

This section focuses on technical AI evaluation and validation concepts without confidential examples or clinical guidance.

- Sensitivity and specificity
- Subject-level or case-level splitting
- Multi-site dataset evaluation
- Device or acquisition variation
- Ground-truth quality
- Segmentation evaluation for medical images
- Model update and re-evaluation principles
- Technical documentation of evidence and limitations

## Phase 5 — Group Evaluation and Robustness

- Dataset group checks
- Group performance analysis
- Performance gap analysis
- Robustness testing
- Distribution shift
- Stress testing under realistic input variation
- Group-specific limitations and mitigations

## Phase 6 — Monitoring and AI Lifecycle Evaluation

- Pre-training checks
- Training monitoring
- Post-training evaluation
- Integration and system-level testing
- Data drift
- Prediction drift
- Re-evaluation after model updates
- Monitoring triggers and lifecycle evidence

## Phase 7 — Advanced AI Evaluation

Status: in progress.

### Completed additions

#### Foundational Large Language Model Evaluation

```text
src/learn_ai_evaluation/llm_metrics.py
examples/llm-evaluation/basic_llm_metrics_example.py
templates/llm-evaluation-report-template.md
tutorials/015-foundational-llm-evaluation/README.md
```

#### Large Vision-Language Model Evaluation

```text
src/learn_ai_evaluation/vlm_metrics.py
examples/vlm-evaluation/basic_vlm_evaluation_example.py
templates/vlm-evaluation-report-template.md
tutorials/016-large-vision-language-model-evaluation/README.md
```

#### Retrieval-Augmented Generation Evaluation

```text
src/learn_ai_evaluation/rag_metrics.py
examples/rag-evaluation/basic_rag_evaluation_example.py
templates/rag-evaluation-report-template.md
tutorials/017-rag-evaluation/README.md
tests/test_rag_metrics.py
```

The RAG phase covers retrieval ranking, Precision@K, Recall@K, reciprocal rank, mean reciprocal rank, average precision, context quality, answer correctness, claim support, citation precision, answerability, abstention, robustness, slice analysis, safety, efficiency, and end-to-end system evaluation.

### Next planned additions

- AI agent evaluation
- Tool-use evaluation
- Agentic workflow evaluation
- Advanced monitoring and lifecycle evaluation for generative systems
