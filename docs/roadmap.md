# Roadmap

This repository is developed gradually using a 7-day learning roadmap. The first phase focuses on classical machine learning evaluation because it provides the foundation for all later topics. The repository has now moved through dataset evaluation and into computer vision evaluation.

## Current tutorials

- 001 What is AI Evaluation?
- 002 Classification Metrics
- 003 Group Performance Evaluation
- 004 Robustness Evaluation
- 008 Dataset Quality Evaluation
- 009 Data Splitting and Leakage
- 010 Computer Vision Evaluation
- 011 Computer Vision Dataset Splits and Failure Review

## Phase 1 — Foundations and Classical ML Evaluation

- What is AI Evaluation?
- Classification Metrics
- Group Performance Evaluation
- Robustness Evaluation
- Confusion Matrix and Threshold Selection
- ROC-AUC and PR-AUC
- Calibration and Confidence
- Dataset Splitting and Leakage
- Cross-Validation
- Error Analysis
- Class Imbalance

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

Status: in progress.

New materials added:

```text
src/learn_ai_evaluation/computer_vision_metrics.py
examples/computer-vision-evaluation/cv_metrics_example.py
templates/computer-vision-evaluation-report-template.md
tutorials/010-computer-vision-evaluation/README.md
tutorials/011-cv-dataset-splits-and-failure-review/README.md
```

Topics covered:

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

This section will focus on technical AI evaluation and validation concepts without using confidential examples.

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
- Subgroup-specific limitations and mitigations

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

- LLM evaluation
- Prompt evaluation
- Factuality evaluation
- VLM evaluation
- RAG retrieval evaluation
- RAG answer evaluation
- AI agent evaluation
- Tool-use evaluation
- Agentic workflow evaluation
