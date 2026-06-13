"""Illustrative VLM SFT skeleton for the workshop-tool task.

The script exits successfully when optional training dependencies or real image files
are unavailable, so lightweight repository validation can still run.
"""

from __future__ import annotations

import json
from pathlib import Path

MODEL_ID = "HuggingFaceTB/SmolVLM2-500M-Video-Instruct"
DATA_PATH = Path("data/small_vlm_tool_inventory_examples.jsonl")
OUTPUT_DIR = Path("outputs/small-vlm-tool-inventory")


def to_conversation(record: dict) -> dict:
    """Convert one metadata record into a multimodal conversation."""
    target_json = json.dumps(record["target"], separators=(",", ":"), sort_keys=True)
    return {
        "image": record["image"],
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image"},
                    {"type": "text", "text": record["prompt"]},
                ],
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": target_json}],
            },
        ],
    }


def load_metadata(path: Path = DATA_PATH) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    records = load_metadata()
    missing_images = [record["image"] for record in records if not Path(record["image"]).exists()]
    if missing_images:
        print("Skipping optional VLM training: replace placeholder image paths with local files.")
        return

    try:
        from datasets import Dataset, Image
        from trl import SFTConfig, SFTTrainer
    except ImportError:
        print("Skipping optional VLM training: install datasets, transformers, trl, accelerate, torch, and pillow.")
        return

    rows = [to_conversation(record) for record in records]
    dataset = Dataset.from_list(rows).cast_column("image", Image())
    split = dataset.train_test_split(test_size=0.2, seed=42)

    config = SFTConfig(
        output_dir=str(OUTPUT_DIR),
        learning_rate=2e-4,
        warmup_ratio=0.03,
        max_grad_norm=1.0,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        num_train_epochs=1,
        max_length=None,
        eval_strategy="steps",
        eval_steps=25,
        save_steps=25,
        logging_steps=5,
        report_to="none",
    )

    trainer = SFTTrainer(
        model=MODEL_ID,
        args=config,
        train_dataset=split["train"],
        eval_dataset=split["test"],
    )
    trainer.train()
    trainer.save_model(str(OUTPUT_DIR / "final"))


if __name__ == "__main__":
    main()
