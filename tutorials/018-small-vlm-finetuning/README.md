# Small-VLM Fine-Tuning for Structured Edge Tasks

This tutorial uses a workshop tool-inventory task to demonstrate how a compact vision-language model can be adapted from general image understanding to structured JSON extraction.

## Why this task

A narrow tool-inventory task is a better fit for a compact local model than unrestricted visual question answering because:

- the object vocabulary can be controlled;
- the output schema is explicit;
- hard negatives can be designed deliberately;
- success can be measured with task-specific metrics;
- local deployment can support offline workshop or maintenance workflows.

## Workflow

```text
Collect and review images
        ↓
Create structured JSON labels
        ↓
Add hard negatives and unusable images
        ↓
Measure the base model
        ↓
Run supervised fine-tuning
        ↓
Evaluate schema, recognition, counting, and abstention
        ↓
Optimise and re-evaluate for edge deployment
```

## Project files

- [`../../docs/small-vlm-tool-inventory-finetuning.md`](../../docs/small-vlm-tool-inventory-finetuning.md)
- [`../../data/small_vlm_tool_inventory_examples.jsonl`](../../data/small_vlm_tool_inventory_examples.jsonl)
- [`../../src/learn_ai_evaluation/small_vlm_tool_inventory.py`](../../src/learn_ai_evaluation/small_vlm_tool_inventory.py)
- [`../../examples/small-vlm-tool-inventory/tool_inventory_evaluation.py`](../../examples/small-vlm-tool-inventory/tool_inventory_evaluation.py)
- [`../../examples/small-vlm-tool-inventory/sft_training_skeleton.py`](../../examples/small-vlm-tool-inventory/sft_training_skeleton.py)
- [`../../tests/test_small_vlm_tool_inventory.py`](../../tests/test_small_vlm_tool_inventory.py)

## Run the lightweight evaluation

```bash
python examples/small-vlm-tool-inventory/tool_inventory_evaluation.py
python -m pytest tests/test_small_vlm_tool_inventory.py -q
```

The SFT skeleton skips successfully until real local image files and optional training dependencies are provided.

## Evaluation gates

Before deployment, require evidence for:

- JSON parse and schema validity;
- tool-name precision, recall, and F1;
- count error;
- hard-negative false positives;
- unsupported visual claims;
- unusable-image abstention;
- latency, peak memory, and throughput;
- retained performance after quantisation or runtime conversion.

## Important limitation

Visible-condition extraction is not a replacement for inspection by a competent person. The model should report only what is visually supported and should use `unknown` when evidence is insufficient.
