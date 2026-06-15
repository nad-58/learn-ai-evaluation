# Computer Vision Model Evaluation

Computer vision evaluation should match the task performed by the model. Image classification, semantic segmentation, and object detection require different outputs, metrics, error analyses, and acceptance criteria.

All examples in this tutorial use small synthetic arrays and bounding boxes so the calculations can be inspected directly.

## Runnable Python examples

Run these commands from the repository root:

```bash
python examples/computer-vision-evaluation/classification_metrics_example.py
python examples/computer-vision-evaluation/segmentation_metrics_example.py
python examples/computer-vision-evaluation/detection_metrics_example.py
python examples/computer-vision-evaluation/cv_metrics_example.py
```

| Example | Coverage |
|---|---|
| [`classification_metrics_example.py`](../../examples/computer-vision-evaluation/classification_metrics_example.py) | Confusion matrix, per-class precision, recall, F1 and macro averages |
| [`segmentation_metrics_example.py`](../../examples/computer-vision-evaluation/segmentation_metrics_example.py) | Pixel accuracy, binary IoU, Dice and multiclass IoU |
| [`detection_metrics_example.py`](../../examples/computer-vision-evaluation/detection_metrics_example.py) | Bounding-box IoU, true/false positives, precision, recall and average precision |
| [`cv_metrics_example.py`](../../examples/computer-vision-evaluation/cv_metrics_example.py) | Combined classification, segmentation and detection demonstration |

Reusable metric implementation:

```text
src/learn_ai_evaluation/computer_vision_metrics.py
```

Tests:

```bash
python -m pytest tests/test_computer_vision_metrics.py -q
```

## 1. Image classification

A classifier assigns one class to each image. The example uses ten images and three classes:

```python
y_true = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2]
y_pred = [0, 0, 1, 1, 1, 0, 2, 2, 1, 2]
```

Create the confusion matrix:

```python
from learn_ai_evaluation.computer_vision_metrics import (
    classification_confusion_matrix,
    per_class_precision_recall_f1,
)

confusion = classification_confusion_matrix(
    y_true,
    y_pred,
    labels=[0, 1, 2],
)
report = per_class_precision_recall_f1(confusion)
```

The confusion matrix uses rows for true classes and columns for predicted classes:

```text
[[2, 1, 0],
 [1, 2, 0],
 [0, 1, 3]]
```

For each class:

```text
precision = TP / (TP + FP)
recall    = TP / (TP + FN)
F1        = 2 × precision × recall / (precision + recall)
```

Report per-class metrics rather than accuracy alone. A high overall accuracy can hide poor performance for a rare class.

### Recommended classification review

- confusion matrix;
- per-class precision, recall and F1;
- macro and weighted averages;
- sensitivity and specificity for binary tasks;
- ROC-AUC and precision-recall curves where probabilities are available;
- calibration and threshold analysis;
- subgroup, site, device and acquisition-condition performance;
- representative false-positive and false-negative examples.

## 2. Binary segmentation

A segmentation model assigns a label to every pixel. The binary example uses two 4 × 4 masks:

```python
import numpy as np

mask_true = np.array(
    [
        [0, 0, 1, 1],
        [0, 1, 1, 1],
        [0, 0, 1, 0],
        [0, 0, 0, 0],
    ]
)

mask_pred = np.array(
    [
        [0, 0, 1, 0],
        [0, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
)
```

Calculate the metrics:

```python
from learn_ai_evaluation.computer_vision_metrics import (
    binary_dice,
    binary_iou,
    pixel_accuracy,
)

print(pixel_accuracy(mask_true, mask_pred))
print(binary_iou(mask_true, mask_pred))
print(binary_dice(mask_true, mask_pred))
```

Definitions:

```text
IoU  = intersection / union
Dice = 2 × intersection / (true positives + predicted positives)
```

For this example:

```text
intersection = 4 pixels
union = 6 pixels
IoU = 4/6 = 0.667
Dice = 8/10 = 0.800
pixel accuracy = 14/16 = 0.875
```

Pixel accuracy can look high when background pixels dominate, so it should not be used alone.

## 3. Multiclass segmentation

For multiclass masks, calculate IoU separately for every class:

```python
from learn_ai_evaluation.computer_vision_metrics import multiclass_iou

scores = multiclass_iou(mask_true, mask_pred)
for class_id, score in scores.items():
    print(class_id, score)
```

Also report:

- mean IoU;
- class frequency and support;
- boundary or surface-distance metrics when shape accuracy matters;
- empty-class handling;
- image-level distributions rather than only pooled pixel totals;
- examples of under-segmentation, over-segmentation and missed objects.

## 4. Object detection

A detection model outputs a class, confidence score and bounding box for each object.

Bounding-box format:

```text
[x_min, y_min, x_max, y_max]
```

Calculate box overlap:

```python
from learn_ai_evaluation.computer_vision_metrics import box_iou

prediction = (12, 12, 48, 48)
ground_truth = (10, 10, 50, 50)
print(box_iou(prediction, ground_truth))
```

A prediction is normally counted as a true positive when:

- image identifier matches;
- predicted and reference classes match;
- the reference box has not already been matched;
- IoU meets the selected threshold.

The runnable example evaluates four predictions against three reference boxes:

```python
from learn_ai_evaluation.computer_vision_metrics import (
    Detection,
    GroundTruthBox,
    detection_summary,
)

summary = detection_summary(
    predictions,
    ground_truth,
    iou_threshold=0.5,
    label="widget",
)
```

The summary reports:

- number of ground-truth objects;
- true positives;
- false positives;
- final precision;
- final recall;
- interpolated average precision;
- IoU threshold.

For stronger detection evaluation, report AP at multiple IoU thresholds, per-class AP, object-size strata, confidence thresholds and missed-object examples.

## 5. Split integrity

Computer vision datasets have additional leakage risks:

- frames from the same video in different splits;
- images from the same subject, scene or acquisition session across splits;
- augmented copies or resized versions in different splits;
- near-duplicate images;
- overlapping image tiles;
- multiple annotations of the same underlying image;
- preprocessing or normalisation fitted on all images.

Use group-aware splitting at the highest relevant entity level. Image hashes, perceptual hashes, embedding similarity and metadata checks can help identify duplication.

## 6. Failure analysis

Metrics should be accompanied by structured review of failures:

```text
classification: false positives, false negatives, class confusion
segmentation: missed regions, boundary errors, fragmentation, over-segmentation
object detection: missed objects, duplicate detections, localisation errors, class errors
```

Analyse failures by:

- class;
- image quality;
- illumination;
- resolution;
- object size;
- occlusion;
- viewpoint;
- site, device or camera;
- subgroup where appropriate;
- confidence score.

## 7. Acceptance criteria

Acceptance criteria should be defined before final testing and linked to intended use. A report should clearly distinguish:

```text
metric target
observed result
confidence interval or uncertainty
subgroup or condition-specific result
pass/fail status
remaining limitation
```

## 8. Reporting checklist

A computer-vision evaluation report should include:

- task and intended use;
- dataset identity and version;
- split methodology and leakage checks;
- class and subgroup support;
- preprocessing and inference configuration;
- selected metrics and rationale;
- per-class and aggregate results;
- threshold selection;
- uncertainty and confidence intervals where appropriate;
- failure examples;
- robustness and distribution-shift testing;
- limitations and release decision.

## Limitations

These examples are intentionally lightweight. Production evaluation may additionally require established benchmark libraries, bootstrap confidence intervals, statistical comparison of model versions, calibration analysis, robustness testing, annotation-quality review, human-factor evaluation and independent validation on representative external data.
