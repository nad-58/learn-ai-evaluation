"""Synthetic medical AI evaluation example.

This example demonstrates technical evaluation for a binary medical AI task using
synthetic data. It is not clinical validation and must not be used to make
medical claims or deployment decisions.

Run from the repository root:

    python examples/medical-ai-evaluation/medical_ai_binary_example.py
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np

# Allow running this example directly from a source checkout without installing
# the package first.
REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from learn_ai_evaluation.medical_ai_evaluation import (  # noqa: E402
    binary_confusion_counts,
    calibration_bins,
    diagnostic_metric_summary,
    expected_calibration_error,
    segmentation_volume_difference,
    select_threshold_for_minimum_sensitivity,
    subgroup_diagnostic_summary,
    threshold_sweep,
)


def print_section(title: str) -> None:
    """Print a section title for a readable command-line example."""
    print("\n" + "=" * len(title))
    print(title)
    print("=" * len(title))


def make_synthetic_binary_data(seed: int = 42) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Create a small synthetic dataset with labels, scores, and groups."""
    rng = np.random.default_rng(seed)

    n_samples = 240
    groups = rng.choice(["site_a", "site_b", "site_c"], size=n_samples, p=[0.45, 0.35, 0.20])

    # Simulate a class imbalance often seen in screening-like examples.
    y_true = rng.binomial(1, p=0.28, size=n_samples)

    # Make positive cases generally score higher, but add group-specific noise
    # to demonstrate why subgroup review is important.
    base_score = np.where(y_true == 1, rng.normal(0.72, 0.16, n_samples), rng.normal(0.28, 0.18, n_samples))
    site_b_shift = np.where(groups == "site_b", -0.06, 0.0)
    site_c_noise = np.where(groups == "site_c", rng.normal(0.0, 0.08, n_samples), 0.0)
    y_score = np.clip(base_score + site_b_shift + site_c_noise, 0.0, 1.0)

    return y_true, y_score, groups


def run_binary_classification_demo() -> None:
    """Run the binary classification evaluation example."""
    y_true, y_score, groups = make_synthetic_binary_data()
    threshold = 0.50

    print_section("Binary classification metrics at a fixed threshold")
    counts = binary_confusion_counts(y_true, y_score, threshold=threshold)
    metrics = diagnostic_metric_summary(counts)
    print(f"Threshold: {threshold:.2f}")
    print(f"Counts: {counts}")
    for name, value in metrics.items():
        print(f"{name:30s}: {value:.3f}")

    print_section("Threshold sweep")
    rows = threshold_sweep(y_true, y_score, thresholds=np.linspace(0.2, 0.8, 7))
    for row in rows:
        print(
            f"threshold={row['threshold']:.2f} | "
            f"sensitivity={row['sensitivity_recall']:.3f} | "
            f"specificity={row['specificity']:.3f} | "
            f"precision={row['precision_ppv']:.3f}"
        )

    print_section("Example threshold selection")
    selected = select_threshold_for_minimum_sensitivity(
        y_true,
        y_score,
        minimum_sensitivity=0.90,
        thresholds=np.linspace(0.2, 0.8, 61),
    )
    print("Selected threshold based on minimum sensitivity target:")
    for key, value in selected.items():
        if isinstance(value, float):
            print(f"{key:30s}: {value:.3f}")
        else:
            print(f"{key:30s}: {value}")

    print_section("Calibration review")
    print(f"Expected calibration error: {expected_calibration_error(y_true, y_score, n_bins=5):.3f}")
    for row in calibration_bins(y_true, y_score, n_bins=5):
        print(
            f"bin=[{row['bin_lower']:.1f}, {row['bin_upper']:.1f}] | "
            f"count={row['count']:3d} | "
            f"mean_score={row['mean_score']:.3f} | "
            f"observed_rate={row['observed_event_rate']:.3f} | "
            f"gap={row['absolute_gap']:.3f}"
        )

    print_section("Subgroup performance")
    subgroup_rows = subgroup_diagnostic_summary(
        y_true,
        y_score,
        groups,
        threshold=threshold,
        minimum_group_size=10,
    )
    for row in subgroup_rows:
        print(
            f"{row.group:8s} | n={row.count:3d} | "
            f"sensitivity={row.sensitivity_recall:.3f} | "
            f"specificity={row.specificity:.3f} | "
            f"precision={row.precision_ppv:.3f} | "
            f"balanced_accuracy={row.balanced_accuracy:.3f}"
        )


def run_segmentation_volume_demo() -> None:
    """Run a tiny segmentation volume-difference example."""
    print_section("Segmentation volume difference")

    reference_mask = np.zeros((8, 8), dtype=int)
    predicted_mask = np.zeros((8, 8), dtype=int)

    reference_mask[2:6, 2:6] = 1
    predicted_mask[2:6, 3:7] = 1

    volume_summary = segmentation_volume_difference(
        reference_mask,
        predicted_mask,
        voxel_volume=1.5,
    )
    for key, value in volume_summary.items():
        print(f"{key:35s}: {value:.3f}")


def main() -> None:
    """Run all example sections."""
    run_binary_classification_demo()
    run_segmentation_volume_demo()


if __name__ == "__main__":
    main()
