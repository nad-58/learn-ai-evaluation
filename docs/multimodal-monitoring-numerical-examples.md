# Numerical Monitoring Examples for Tabular, Image, and Speech Data

This guide demonstrates lifecycle monitoring using three data modalities. Every dataset is synthetic, small, inspectable, and stored in CSV format.

## Run the complete example

```bash
python examples/monitoring-and-lifecycle/multimodal_monitoring_example.py
```

Run the tests:

```bash
python -m pytest tests/test_multimodal_monitoring.py -q
```

## Data files

```text
data/monitoring/tabular_reference.csv
data/monitoring/tabular_current.csv
data/monitoring/image_reference.csv
data/monitoring/image_current.csv
data/monitoring/speech_reference.csv
data/monitoring/speech_current.csv
```

## 1. Tabular monitoring data

The reference and current files each contain 12 records with:

```text
record_id
age
score
latency_ms
prediction
```

Reference ranges include:

```text
age:        24 to 70
score:      0.42 to 0.91
latency_ms: 38 to 48
```

The current window intentionally shifts the distributions:

```text
age:        36 to 80
score:      0.38 to 0.86
latency_ms: 49 to 64
```

The example calculates Population Stability Index for `age`, `score`, and `latency_ms`:

```python
from learn_ai_evaluation.monitoring_lifecycle import feature_drift_report

report = feature_drift_report(
    reference_df,
    current_df,
    ["age", "score", "latency_ms"],
    bins=4,
)
```

Flow:

```text
reference rows + current rows
-> same feature schema
-> PSI calculation
-> feature-level drift flag
-> investigation decision
```

## 2. Image monitoring data

The image files contain two 8 by 8 grayscale matrices. Pixel values are normalised to the range 0 to 1.

The current image is intentionally brighter than the reference image. The monitoring utility extracts:

```text
mean intensity
standard deviation of intensity
minimum intensity
maximum intensity
bright-pixel rate
mean edge magnitude
```

Python:

```python
from learn_ai_evaluation.multimodal_monitoring import image_summary_features

reference_features = image_summary_features(reference_image)
current_features = image_summary_features(current_image)
```

Definitions:

```text
mean intensity = sum of pixel values / number of pixels
bright-pixel rate = pixels >= 0.75 / total pixels
mean edge magnitude = mean absolute difference between neighbouring pixels
```

Flow:

```text
reference image + current image
-> extract comparable quality features
-> calculate absolute and relative changes
-> review acquisition or preprocessing shift
```

The features are monitoring indicators rather than task-performance metrics. A brightness shift may be harmless, or it may indicate a changed camera, scanner, exposure setting, preprocessing pipeline, or operating environment.

## 3. Speech and audio monitoring data

The speech files contain two synthetic 32-sample waveforms at an assumed sample rate of 8,000 Hz.

The reference waveform represents a 1,000 Hz sinusoidal pattern with peak amplitude 1.0. The current waveform represents a 2,000 Hz pattern with peak amplitude 0.7.

The utility calculates:

```text
mean amplitude
root-mean-square amplitude
peak amplitude
zero-crossing rate
dominant frequency
```

Python:

```python
from learn_ai_evaluation.multimodal_monitoring import audio_summary_features

reference_features = audio_summary_features(reference_samples, sample_rate=8000)
current_features = audio_summary_features(current_samples, sample_rate=8000)
```

Definitions:

```text
RMS amplitude = sqrt(mean(sample squared))
peak amplitude = maximum absolute sample value
zero-crossing rate = sign changes / adjacent sample pairs
dominant frequency = largest non-zero FFT magnitude
```

Expected numerical behaviour:

```text
reference dominant frequency: 1000 Hz
current dominant frequency:   2000 Hz
reference peak amplitude:     1.0
current peak amplitude:       0.7
```

Flow:

```text
reference waveform + current waveform
-> extract amplitude and frequency features
-> compare current with baseline
-> investigate microphone, codec, noise, sampling, or population changes
```

## 4. Feature comparison

The shared comparison function reports:

```text
feature
reference value
current value
absolute change
relative change
```

Relative change is calculated as:

```text
(current - reference) / absolute(reference)
```

Use:

```python
from learn_ai_evaluation.multimodal_monitoring import compare_feature_sets

rows = compare_feature_sets(reference_features, current_features)
```

## 5. Monitoring interpretation

A detected change is not automatically a model failure. The correct sequence is:

```text
1. Confirm data quality and pipeline integrity.
2. Check whether the change is expected or authorised.
3. Examine model performance and subgroup effects.
4. Review operational conditions and incidents.
5. Apply warning or action thresholds.
6. Investigate root cause.
7. Mitigate, retrain, restrict use, or revalidate when needed.
```

## 6. Additional modality-specific signals

### Images

- image dimensions and aspect ratio;
- bit depth;
- brightness and contrast;
- blur or focus;
- compression artifacts;
- colour-channel distribution;
- acquisition device and protocol;
- embedding drift;
- segmentation or detection confidence.

### Speech and audio

- duration;
- sample rate;
- clipping rate;
- silence rate;
- signal-to-noise ratio;
- RMS energy;
- spectral centroid;
- dominant-frequency distribution;
- language, accent, microphone, codec, and environment;
- word-error rate when reference transcripts are available.

### Time series and sensors

- missing intervals;
- sampling frequency;
- flat-line rate;
- saturation;
- mean, variance, and quantiles;
- trend and seasonality;
- frequency-domain features;
- sensor or device identifiers;
- alert and anomaly rates.

## 7. Limitations

These datasets are intentionally small and demonstrate calculation flow. Production monitoring requires representative sample sizes, time-aware windows, confidence intervals, robust data validation, privacy controls, model-performance labels, subgroup analysis, incident review, and risk-based thresholds.
