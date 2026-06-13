"""Illustrative VLM SFT skeleton for the workshop-tool task.

This file is intentionally excluded from lightweight CI because it requires a GPU,
real image files, and optional Hugging Face training dependencies.
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
    try:
        from datasets import Dataset, Image
        from trl import SFTConfig, SFTTrainer
    except ImportError as exc:
        raise SystemExit(
            "Install optional training dependencies: datasets, transformers, trl, accelerate, torch, pillow"
        ) from exc

    rows = [to_conversation(record) for record in load_metadata()]
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
        assistant_only_loss=True,
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
