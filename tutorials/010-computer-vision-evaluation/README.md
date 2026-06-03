# 010 — Computer Vision Evaluation

Computer vision evaluation checks whether a model works reliably on images, masks, boxes, frames, or visual scenes. It should not stop at one headline number. A good evaluation explains what was tested, how the test data was split, which metrics were used, and what types of failures were observed.

This tutorial is public-safe and uses general technical examples only.

## Learning goals

By the end of this tutorial, you should be able to:

- select task-appropriate metrics for image classification, segmentation, and object detection;
- explain IoU, Dice, pixel accuracy, precision, recall, and average precision;
- identify common computer vision split and leakage risks;
- review visual failure cases in a structured way;
- document limitations and next actions.

## 1. Start with the task type

Different computer vision tasks require different metrics.

| Task | Typical output | Useful metrics |
|---|---|---|
| Image classification | one or more labels per image | accuracy, precision, recall, F1, ROC-AUC, PR-AUC, calibration |
| Semantic segmentation | class label for each pixel | IoU, Dice, pixel accuracy, per-class recall |
| Object detection | boxes, labels, and confidence scores | IoU, precision, recall, AP, mAP |
| Instance segmentation | masks for each object instance | mask IoU, Dice, AP, object-level recall |
| Visual quality or enhancement | transformed image | task metric plus visual quality and downstream impact checks |

## 2. Image classification evaluation

For image classification, the confusion matrix is often the best starting point. It shows which classes are confused with each other.

Important checks:

- report per-class precision and recall, not only overall accuracy;
- check whether minority classes have enough support;
- review examples of false positives and false negatives;
- consider threshold tuning when the model outputs probabilities;
- inspect confidence calibration when predictions are used for decision support.

Common risk: a high accuracy score can hide poor performance on rare classes.

## 3. Segmentation evaluation

Segmentation metrics compare predicted masks with ground-truth masks.

### Intersection over Union

IoU measures the overlap between the predicted region and the ground-truth region.

```text
IoU = intersection / union
```

IoU is strict. Small boundary errors can reduce the score, especially for small regions.

### Dice score

Dice also measures overlap but gives more weight to the intersection.

```text
Dice = 2 * intersection / (predicted area + ground-truth area)
```

Dice is widely used for region overlap, but it should still be interpreted with visual review.

### Pixel accuracy

Pixel accuracy measures the percentage of correctly classified pixels. It can be misleading when the background dominates the image.

## 4. Object detection evaluation

Object detection evaluation checks whether predicted boxes match ground-truth boxes.

A predicted box is usually considered a true positive when:

1. the predicted class is correct;
2. the predicted box overlaps the ground-truth box above a chosen IoU threshold;
3. the ground-truth object has not already been matched by a higher-confidence prediction.

Important reporting choices:

- confidence threshold;
- IoU threshold;
- non-maximum suppression settings;
- per-class precision and recall;
- small, medium, and large object performance where relevant.

## 5. Dataset split risks in computer vision

Computer vision data can contain strong correlations. Leakage can occur when similar images appear in both training and testing.

Examples:

- adjacent video frames split across train and test;
- crops from the same original image in different splits;
- multiple images of the same object, person, product, or scene split incorrectly;
- near-duplicate images downloaded from public sources;
- images from the same capture session or camera mixed across splits;
- augmented versions of an image appearing outside the training split.

A safer split may need to be based on subject, object, scene, location, video, capture session, or time rather than individual image files.

## 6. Visual failure-case review

Metrics tell you what happened numerically. Visual review helps explain why.

Useful failure categories include:

- blur or motion artefact;
- poor lighting;
- low contrast;
- occlusion;
- unusual scale or orientation;
- small objects;
- confusing background;
- ambiguous labels;
- boundary uncertainty;
- preprocessing artefacts.

A good evaluation report should include representative examples or a structured summary of these failures. Do not publish private or sensitive images in a public repository.

## 7. Run the example

From the repository root:

```bash
python examples/computer-vision-evaluation/cv_metrics_example.py
```

The example demonstrates:

- classification confusion matrix and macro F1;
- binary IoU and Dice;
- multiclass segmentation IoU;
- object detection IoU, precision, recall, and average precision.

## 8. Use the template

Use this template for a structured report:

```text
templates/computer-vision-evaluation-report-template.md
```

## Key takeaway

Computer vision evaluation should combine metrics, split-risk analysis, visual failure review, and robustness checks. The final question is not only whether the model performs well on average, but also where, why, and under what visual conditions it fails.
