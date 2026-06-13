import json
from pathlib import Path

from learn_ai_evaluation.small_vlm_tool_inventory import (
    hard_negative_false_positive_rate,
    schema_validity_rate,
    tool_count_mae,
    tool_name_f1,
)

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "small_vlm_tool_inventory_examples.jsonl"


def load_records():
    return [json.loads(line) for line in DATA.read_text(encoding="utf-8").splitlines() if line.strip()]


def main():
    references = [row["target"] for row in load_records()]
    predictions = [dict(item) for item in references]
    predictions[1] = dict(predictions[1])
    predictions[1]["tools"] = [dict(tool) for tool in predictions[1]["tools"]]
    predictions[1]["tools"][1]["count"] = 5
    predictions[3] = dict(predictions[3])
    predictions[3]["tools"] = [{"name": "pliers", "count": 1, "visible_condition": "unknown", "confidence": 0.51}]

    name_f1 = sum(tool_name_f1(a, b) for a, b in zip(references, predictions)) / len(references)
    count_mae = sum(tool_count_mae(a, b) for a, b in zip(references, predictions)) / len(references)
    print(f"schema_validity_rate={schema_validity_rate(predictions):.3f}")
    print(f"mean_tool_name_f1={name_f1:.3f}")
    print(f"mean_tool_count_mae={count_mae:.3f}")
    print(f"hard_negative_false_positive_rate={hard_negative_false_positive_rate(predictions):.3f}")


if __name__ == "__main__":
    main()
