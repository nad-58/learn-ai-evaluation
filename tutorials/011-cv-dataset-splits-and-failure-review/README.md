# 011 — Computer Vision Dataset Splits and Failure Review

Computer vision evaluation is strongly affected by how the dataset is split and how failures are reviewed. Two models can report similar headline metrics while having very different real-world behaviour.

This tutorial focuses on practical checks that should be performed before trusting computer vision metrics.

## 1. Why image-level random splitting can be risky

A random image-level split is not always independent. In many projects, several images may be highly related even when they have different file names.

Common examples include:

- multiple frames from the same video;
- several crops from the same original image;
- burst-mode photos from the same scene;
- repeated images of the same object or product;
- images from the same capture session;
- augmented copies of the same image;
- near-duplicates collected from public sources.

When related images appear in both training and testing, evaluation results can look better than they should.

## 2. Choose the correct split unit

Select the split unit based on the independence requirement of the task.

| Scenario | Safer split unit |
|---|---|
| Video frames | video, sequence, or time block |
| Multiple images per object | object ID or product ID |
| Multiple images per person or subject | subject ID |
| Images from different sites or cameras | site, camera, or acquisition source |
| Remote-sensing or geospatial imagery | location or time period |
| Industrial inspection | batch, production run, device, or capture setup |

The split should match the question the evaluation is trying to answer.

## 3. Near-duplicate checks

Exact duplicates are easy to find using hashes. Near-duplicates are more difficult because resizing, compression, cropping, or brightness changes may alter the file while preserving the visual content.

Useful checks include:

- exact file hash comparison;
- perceptual hash comparison;
- embedding similarity search;
- manual review of high-similarity examples;
- checking repeated metadata such as capture time, camera ID, or source file.

## 4. Visual failure-case review

A structured failure review should connect metric errors to visual causes.

Suggested categories:

| Failure category | Example question |
|---|---|
| Lighting | Does performance drop in dark, bright, or uneven lighting? |
| Blur | Does motion blur cause missed detections or wrong classes? |
| Scale | Are small objects or small regions missed? |
| Occlusion | Are partly hidden objects handled correctly? |
| Boundary ambiguity | Are segmentation boundaries consistently defined? |
| Background shortcut | Is the model relying on irrelevant background context? |
| Preprocessing artefact | Does resizing, cropping, or compression change the prediction? |

## 5. Failure-case table

Use a simple table to make failure review actionable.

| Case ID | Input condition | Ground truth | Prediction | Error type | Likely cause | Action |
|---|---|---|---|---|---|---|
| example-001 | low contrast | class A | class B | false negative | weak boundary | add contrast test set |
| example-002 | small object | object present | no detection | missed detection | object too small | report size-specific recall |

Do not publish private or sensitive images in a public repository. Use synthetic examples or anonymised summaries.

## 6. Questions to answer before reporting final metrics

- Was the test set independent from the training set?
- Was the split performed at the correct unit?
- Were duplicates and near-duplicates checked?
- Were class, object-size, and capture-condition distributions reviewed?
- Were false positives and false negatives inspected visually?
- Were threshold choices documented?
- Were limitations written clearly?

## Key takeaway

Computer vision evaluation is not only a metric calculation problem. The credibility of the metric depends on data independence, label quality, visual review, and transparent documentation of limitations.
