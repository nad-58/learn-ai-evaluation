"""Medical AI split and leakage utilities for Learn AI Evaluation.

This module is public-safe and educational. It demonstrates why medical AI
projects often need patient-level, subject-level, site-level, or time-aware data
splits rather than simple random row-level splits.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np


@dataclass(frozen=True)
class SplitLeakageReport:
    """Summary of entity overlap between train, validation, and test splits."""

    entity_name: str
    train_count: int
    validation_count: int
    test_count: int
    train_validation_overlap: int
    train_test_overlap: int
    validation_test_overlap: int
    any_overlap: bool


def _as_set(values: Iterable[str]) -> set[str]:
    """Convert values to a set of strings."""
    return {str(value) for value in values}


def check_entity_overlap(
    train_entities: Iterable[str],
    validation_entities: Iterable[str],
    test_entities: Iterable[str],
    entity_name: str = "patient",
) -> SplitLeakageReport:
    """Check whether the same entity appears across data splits.

    In medical AI, one patient, subject, study, encounter, site, scanner, or
    acquisition episode can generate multiple rows or images. If related samples
    are split across train and test sets, performance can be over-optimistic.
    """
    train = _as_set(train_entities)
    validation = _as_set(validation_entities)
    test = _as_set(test_entities)

    tv = train & validation
    tt = train & test
    vt = validation & test

    return SplitLeakageReport(
        entity_name=entity_name,
        train_count=len(train),
        validation_count=len(validation),
        test_count=len(test),
        train_validation_overlap=len(tv),
        train_test_overlap=len(tt),
        validation_test_overlap=len(vt),
        any_overlap=bool(tv or tt or vt),
    )


def grouped_random_split(
    group_ids: Sequence[str],
    train_fraction: float = 0.7,
    validation_fraction: float = 0.15,
    seed: int = 42,
) -> dict[str, np.ndarray]:
    """Create train/validation/test indices while keeping groups together.

    Parameters
    ----------
    group_ids:
        One group ID per sample. This may represent patient ID, subject ID,
        study ID, site ID, scanner ID, or another independence unit.
    train_fraction:
        Fraction of unique groups assigned to training.
    validation_fraction:
        Fraction of unique groups assigned to validation.
    seed:
        Random seed for reproducibility.
    """
    if not 0 < train_fraction < 1:
        raise ValueError("train_fraction must be between 0 and 1")
    if not 0 <= validation_fraction < 1:
        raise ValueError("validation_fraction must be between 0 and 1")
    if train_fraction + validation_fraction >= 1:
        raise ValueError("train_fraction + validation_fraction must be less than 1")

    groups = np.asarray(group_ids).astype(str)
    unique_groups = np.array(sorted(set(groups.tolist())))
    rng = np.random.default_rng(seed)
    rng.shuffle(unique_groups)

    n_groups = len(unique_groups)
    n_train = int(round(n_groups * train_fraction))
    n_validation = int(round(n_groups * validation_fraction))

    train_groups = set(unique_groups[:n_train])
    validation_groups = set(unique_groups[n_train:n_train + n_validation])
    test_groups = set(unique_groups[n_train + n_validation:])

    train_indices = np.where(np.isin(groups, list(train_groups)))[0]
    validation_indices = np.where(np.isin(groups, list(validation_groups)))[0]
    test_indices = np.where(np.isin(groups, list(test_groups)))[0]

    return {
        "train_indices": train_indices,
        "validation_indices": validation_indices,
        "test_indices": test_indices,
        "train_groups": np.array(sorted(train_groups)),
        "validation_groups": np.array(sorted(validation_groups)),
        "test_groups": np.array(sorted(test_groups)),
    }


def summarize_split_balance(
    y: Sequence[int],
    indices: Sequence[int],
) -> dict[str, float | int]:
    """Summarise class balance for one split."""
    labels = np.asarray(y).astype(int)
    split_indices = np.asarray(indices).astype(int)
    selected = labels[split_indices]
    count = int(selected.size)
    positive_count = int(np.sum(selected == 1))
    negative_count = int(np.sum(selected == 0))
    return {
        "count": count,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "positive_fraction": float(positive_count / count) if count else 0.0,
    }


def time_ordered_group_split(
    group_ids: Sequence[str],
    timestamps: Sequence[float],
    train_fraction: float = 0.7,
    validation_fraction: float = 0.15,
) -> dict[str, np.ndarray]:
    """Create a time-aware split based on first timestamp per group.

    This is useful when the evaluation should simulate future data. Groups are
    sorted by their earliest timestamp and then assigned to train, validation,
    and test sets without splitting a group across phases.
    """
    if len(group_ids) != len(timestamps):
        raise ValueError("group_ids and timestamps must have the same length")

    groups = np.asarray(group_ids).astype(str)
    times = np.asarray(timestamps).astype(float)
    unique_groups = sorted(set(groups.tolist()), key=lambda g: float(np.min(times[groups == g])))

    n_groups = len(unique_groups)
    n_train = int(round(n_groups * train_fraction))
    n_validation = int(round(n_groups * validation_fraction))

    train_groups = set(unique_groups[:n_train])
    validation_groups = set(unique_groups[n_train:n_train + n_validation])
    test_groups = set(unique_groups[n_train + n_validation:])

    return {
        "train_indices": np.where(np.isin(groups, list(train_groups)))[0],
        "validation_indices": np.where(np.isin(groups, list(validation_groups)))[0],
        "test_indices": np.where(np.isin(groups, list(test_groups)))[0],
        "train_groups": np.array(sorted(train_groups)),
        "validation_groups": np.array(sorted(validation_groups)),
        "test_groups": np.array(sorted(test_groups)),
    }
