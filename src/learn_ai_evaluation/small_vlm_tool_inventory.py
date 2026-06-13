"""Evaluation utilities for a structured workshop-tool VLM task."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence

_ALLOWED_CONDITIONS = {"good", "worn", "damaged", "unknown"}
_REQUIRED_TOP_LEVEL = {
    "scene_type",
    "relevant",
    "tools",
    "safety_observations",
    "unknown_items",
    "image_quality",
}


def validate_tool_inventory(output: Mapping[str, object]) -> list[str]:
    """Return schema and value errors for one structured VLM output."""
    errors: list[str] = []
    missing = _REQUIRED_TOP_LEVEL - set(output)
    if missing:
        errors.append(f"missing keys: {sorted(missing)}")

    if not isinstance(output.get("scene_type"), str):
        errors.append("scene_type must be a string")
    if not isinstance(output.get("relevant"), bool):
        errors.append("relevant must be a boolean")

    tools = output.get("tools")
    if not isinstance(tools, list):
        errors.append("tools must be a list")
    else:
        for index, tool in enumerate(tools):
            prefix = f"tools[{index}]"
            if not isinstance(tool, Mapping):
                errors.append(f"{prefix} must be an object")
                continue
            if not isinstance(tool.get("name"), str) or not tool.get("name"):
                errors.append(f"{prefix}.name must be a non-empty string")
            count = tool.get("count")
            if not isinstance(count, int) or isinstance(count, bool) or count < 1:
                errors.append(f"{prefix}.count must be a positive integer")
            condition = tool.get("visible_condition")
            if condition not in _ALLOWED_CONDITIONS:
                errors.append(
                    f"{prefix}.visible_condition must be one of {sorted(_ALLOWED_CONDITIONS)}"
                )
            confidence = tool.get("confidence")
            if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
                errors.append(f"{prefix}.confidence must be numeric")
            elif not 0.0 <= float(confidence) <= 1.0:
                errors.append(f"{prefix}.confidence must be between 0 and 1")

    for key in ("safety_observations", "unknown_items"):
        value = output.get(key)
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            errors.append(f"{key} must be a list of strings")

    quality = output.get("image_quality")
    if not isinstance(quality, Mapping):
        errors.append("image_quality must be an object")
    else:
        if quality.get("status") not in {"usable", "limited", "unusable"}:
            errors.append("image_quality.status must be usable, limited, or unusable")
        if not isinstance(quality.get("notes"), str):
            errors.append("image_quality.notes must be a string")

    if output.get("relevant") is False and isinstance(tools, list) and tools:
        errors.append("irrelevant scenes must not contain predicted tools")
    return errors


def schema_validity_rate(outputs: Iterable[Mapping[str, object]]) -> float:
    """Return the fraction of outputs that satisfy the schema."""
    rows = list(outputs)
    return sum(not validate_tool_inventory(row) for row in rows) / len(rows) if rows else 0.0


def _tool_counts(output: Mapping[str, object]) -> dict[str, int]:
    counts: dict[str, int] = {}
    tools = output.get("tools", [])
    if not isinstance(tools, list):
        return counts
    for tool in tools:
        if isinstance(tool, Mapping) and isinstance(tool.get("name"), str):
            name = tool["name"].strip().lower()
            count = tool.get("count", 0)
            if isinstance(count, int) and not isinstance(count, bool):
                counts[name] = counts.get(name, 0) + count
    return counts


def tool_name_f1(reference: Mapping[str, object], prediction: Mapping[str, object]) -> float:
    """Compute set-based F1 over normalized tool names."""
    ref = set(_tool_counts(reference))
    pred = set(_tool_counts(prediction))
    if not ref and not pred:
        return 1.0
    if not ref or not pred:
        return 0.0
    overlap = len(ref & pred)
    precision = overlap / len(pred)
    recall = overlap / len(ref)
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0


def tool_count_mae(reference: Mapping[str, object], prediction: Mapping[str, object]) -> float:
    """Compute mean absolute count error across the union of tool names."""
    ref = _tool_counts(reference)
    pred = _tool_counts(prediction)
    names = sorted(set(ref) | set(pred))
    return sum(abs(ref.get(name, 0) - pred.get(name, 0)) for name in names) / len(names) if names else 0.0


def hard_negative_false_positive_rate(outputs: Sequence[Mapping[str, object]]) -> float:
    """Measure tool false positives on records labelled as irrelevant scenes."""
    negatives = [row for row in outputs if row.get("relevant") is False]
    if not negatives:
        return 0.0
    false_positives = sum(bool(_tool_counts(row)) for row in negatives)
    return false_positives / len(negatives)
