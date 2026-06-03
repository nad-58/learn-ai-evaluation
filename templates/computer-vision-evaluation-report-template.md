# Computer Vision Evaluation Report Template

This template is for public-safe technical evaluation of computer vision models. It is suitable for educational projects, internal model reviews, and portfolio demonstrations using synthetic or public datasets.

Do not include confidential datasets, client names, private images, protected personal data, or proprietary acceptance criteria.

## 1. Evaluation summary

- Project or model name:
- Task type: image classification / object detection / segmentation / multi-task / other
- Model version:
- Dataset version:
- Evaluation date:
- Evaluator:
- Intended evaluation purpose:

## 2. Task definition

Describe the vision task in plain language.

- What is the input?
- What is the output?
- What classes, objects, or regions are evaluated?
- What is outside the intended scope?
- What failure types are most important to detect?

## 3. Dataset and split description

- Number of images:
- Number of subjects, scenes, devices, sites, or capture conditions, where relevant:
- Number of classes or labels:
- Training / validation / test split sizes:
- Split unit: image-level / video-level / subject-level / scene-level / location-level / time-level
- Duplicate or near-duplicate image checks performed:
- Leakage risks considered:

### Split-risk notes

Computer vision datasets often contain correlated samples. Examples include adjacent video frames, crops from the same original image, multiple images from the same object, or repeated captures from the same scene. Document how these were handled.

## 4. Ground truth and annotation quality

- Annotation source:
- Annotation tool or workflow:
- Number of annotators:
- Quality-control checks:
- Known ambiguous classes or boundaries:
- Inter-annotator agreement, where available:
- Label corrections or exclusions:

## 5. Image preprocessing

- Resizing or cropping:
- Normalisation:
- Colour handling:
- Augmentation used during training:
- Preprocessing used during evaluation:
- Any difference between training and evaluation preprocessing:

## 6. Image classification metrics

Use this section when the task is image classification.

| Metric | Result | Notes |
|---|---:|---|
| Accuracy |  |  |
| Macro precision |  |  |
| Macro recall |  |  |
| Macro F1 |  |  |
| Weighted F1 |  |  |
| ROC-AUC, if applicable |  |  |
| PR-AUC, if applicable |  |  |
| Calibration metric, if applicable |  |  |

Add confusion matrix and per-class performance.

| Class | Support | Precision | Recall | F1 | Main error mode |
|---|---:|---:|---:|---:|---|
|  |  |  |  |  |  |

## 7. Segmentation metrics

Use this section when the task is semantic, instance, or binary segmentation.

| Class or region | Support / pixels / cases | IoU | Dice | Pixel accuracy | Notes |
|---|---:|---:|---:|---:|---|
|  |  |  |  |  |  |

Document whether metrics are calculated per image and averaged, or calculated globally across all pixels.

## 8. Object detection metrics

Use this section when the task is object detection.

| Class | Ground-truth objects | Predictions | IoU threshold | Precision | Recall | AP | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
|  |  |  |  |  |  |  |  |

Document confidence thresholds, non-maximum suppression settings, IoU thresholds, and whether small, medium, and large objects were evaluated separately.

## 9. Visual failure-case review

Summarise visual inspection of errors.

| Failure case ID | Task type | Description | Possible cause | Action |
|---|---|---|---|---|
|  |  |  |  |  |

Common examples:

- Poor lighting or blur
- Occlusion
- Low contrast
- Small objects
- Borderline labels
- Unusual orientation
- Background shortcut learning
- Cropping or resizing artefacts

## 10. Robustness and input variation

| Variation tested | Method | Result | Risk level | Notes |
|---|---|---|---|---|
| Brightness/contrast |  |  |  |  |
| Blur/noise |  |  |  |  |
| Rotation/scale |  |  |  |  |
| Compression |  |  |  |  |
| Different camera/device/source |  |  |  |  |

## 11. Decision thresholds

- Classification threshold:
- Detection confidence threshold:
- Segmentation probability threshold:
- Rationale for selected thresholds:
- Trade-off between false positives and false negatives:

## 12. Evaluation limitations

List known limitations, such as small test set, limited capture conditions, weak labels, missing subgroup analysis, or incomplete stress testing.

## 13. Recommended next actions

- Additional data checks:
- Additional metric analysis:
- Additional failure-case review:
- Additional robustness testing:
- Changes before deployment or wider use:
