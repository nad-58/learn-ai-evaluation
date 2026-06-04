"""Patient-level split and leakage example for medical AI evaluation.

This example uses synthetic data to show why row-level random splitting can be
unsafe when several samples belong to the same patient or subject.

Run from the repository root:

    python examples/medical-ai-evaluation/patient_level_split_example.py
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = REPO_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from learn_ai_evaluation.medical_ai_splits import (  # noqa: E402
    check_entity_overlap,
    grouped_random_split,
    summarize_split_balance,
    time_ordered_group_split,
)


def make_synthetic_samples(seed: int = 7) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Create sample IDs, patient IDs, labels, and timestamps."""
    rng = np.random.default_rng(seed)
    patient_ids = []
    labels = []
    timestamps = []

    for patient_index in range(60):
        patient = f"patient_{patient_index:03d}"
        n_samples = int(rng.integers(1, 5))
        patient_label = int(rng.binomial(1, 0.30))
        first_time = float(patient_index)
        for sample_index in range(n_samples):
            patient_ids.append(patient)
            labels.append(patient_label)
            timestamps.append(first_time + sample_index * 0.01)

    return np.asarray(patient_ids), np.asarray(labels), np.asarray(timestamps)


def row_level_split(patient_ids: np.ndarray, seed: int = 7) -> dict[str, np.ndarray]:
    """Create an intentionally unsafe row-level split for demonstration."""
    rng = np.random.default_rng(seed)
    indices = np.arange(len(patient_ids))
    rng.shuffle(indices)
    n_train = int(round(len(indices) * 0.7))
    n_val = int(round(len(indices) * 0.15))
    return {
        "train_indices": indices[:n_train],
        "validation_indices": indices[n_train:n_train + n_val],
        "test_indices": indices[n_train + n_val:],
    }


def print_report(title: str, patient_ids: np.ndarray, labels: np.ndarray, split: dict[str, np.ndarray]) -> None:
    """Print leakage and class-balance summary for one split."""
    print("\n" + "=" * len(title))
    print(title)
    print("=" * len(title))

    report = check_entity_overlap(
        train_entities=patient_ids[split["train_indices"]],
        validation_entities=patient_ids[split["validation_indices"]],
        test_entities=patient_ids[split["test_indices"]],
        entity_name="patient",
    )
    print(report)

    for split_name in ["train_indices", "validation_indices", "test_indices"]:
        summary = summarize_split_balance(labels, split[split_name])
        print(f"{split_name:20s}: {summary}")


def main() -> None:
    patient_ids, labels, timestamps = make_synthetic_samples()

    unsafe_split = row_level_split(patient_ids)
    print_report("Unsafe row-level split", patient_ids, labels, unsafe_split)

    patient_level_split = grouped_random_split(patient_ids, seed=7)
    print_report("Safer patient-level split", patient_ids, labels, patient_level_split)

    temporal_split = time_ordered_group_split(patient_ids, timestamps)
    print_report("Time-aware patient-level split", patient_ids, labels, temporal_split)

    print("\nInterpretation:")
    print("A useful medical AI split should normally keep the independence unit together.")
    print("For imaging or longitudinal data, this may be the patient, subject, study, site, scanner, or episode.")


if __name__ == "__main__":
    main()
