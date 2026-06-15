"""Simple public-safe monitoring utilities for tabular, image, and audio data."""
from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def image_summary_features(image: Sequence[Sequence[float]]) -> dict[str, float]:
    """Return transparent summary features for a grayscale image matrix."""
    array = np.asarray(image, dtype=float)
    if array.ndim != 2 or array.size == 0:
        raise ValueError("image must be a non-empty two-dimensional matrix")
    if np.any(~np.isfinite(array)):
        raise ValueError("image must contain only finite values")

    horizontal = np.abs(np.diff(array, axis=1))
    vertical = np.abs(np.diff(array, axis=0))
    edge_values = np.concatenate([horizontal.ravel(), vertical.ravel()])

    return {
        "mean_intensity": float(array.mean()),
        "std_intensity": float(array.std(ddof=0)),
        "minimum_intensity": float(array.min()),
        "maximum_intensity": float(array.max()),
        "bright_pixel_rate": float(np.mean(array >= 0.75)),
        "mean_edge_magnitude": float(edge_values.mean()) if edge_values.size else 0.0,
    }


def audio_summary_features(
    samples: Sequence[float],
    sample_rate: float,
) -> dict[str, float]:
    """Return basic waveform features for a one-dimensional audio signal."""
    signal = np.asarray(samples, dtype=float)
    if signal.ndim != 1 or signal.size < 2:
        raise ValueError("samples must be a one-dimensional signal with at least two values")
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    if np.any(~np.isfinite(signal)):
        raise ValueError("samples must contain only finite values")

    rms = float(np.sqrt(np.mean(signal**2)))
    peak = float(np.max(np.abs(signal)))
    zero_crossings = np.count_nonzero(np.diff(np.signbit(signal)))
    zero_crossing_rate = float(zero_crossings / (len(signal) - 1))

    centred = signal - signal.mean()
    spectrum = np.abs(np.fft.rfft(centred))
    frequencies = np.fft.rfftfreq(len(signal), d=1.0 / sample_rate)
    dominant_frequency = float(frequencies[int(np.argmax(spectrum[1:])) + 1]) if len(spectrum) > 1 else 0.0

    return {
        "mean_amplitude": float(signal.mean()),
        "rms_amplitude": rms,
        "peak_amplitude": peak,
        "zero_crossing_rate": zero_crossing_rate,
        "dominant_frequency_hz": dominant_frequency,
    }


def relative_change(reference: float, current: float) -> float:
    """Return relative change from reference to current."""
    if reference == 0:
        return float("nan") if current == 0 else float("inf")
    return float((current - reference) / abs(reference))


def compare_feature_sets(
    reference: dict[str, float],
    current: dict[str, float],
) -> list[dict[str, float | str]]:
    """Compare matching numerical features from two monitoring windows."""
    if set(reference) != set(current):
        raise ValueError("reference and current feature names must match")
    rows: list[dict[str, float | str]] = []
    for feature in sorted(reference):
        ref = float(reference[feature])
        cur = float(current[feature])
        rows.append(
            {
                "feature": feature,
                "reference": ref,
                "current": cur,
                "absolute_change": cur - ref,
                "relative_change": relative_change(ref, cur),
            }
        )
    return rows
