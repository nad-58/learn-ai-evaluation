# Small-VLM Fine-Tuning Case Study: Workshop Tool Inventory

This case study adapts the small-VLM fine-tuning workflow from food extraction to a different edge-AI task: **structured workshop-tool inventory and visible-condition inspection**.

## 1. Task definition

Input:

- one image of a workbench, toolbox, maintenance area, or hard-negative scene;
- one short instruction requesting structured extraction.

Output:

```json
{
  "scene_type": "workbench",
  "relevant": true,
  "tools": [
    {
      "name": "adjustable wrench",
      "count": 1,
      "visible_condition": "good",
      "confidence": 0.96
    }
  ],
  "safety_observations": [
    "one item is close to the bench edge"
  ],
  "unknown_items": [],
  "image_quality": {
    "status": "usable",
    "notes": "clear overhead view"
  }
}
```

The model should identify only **visually supported** objects. It must not infer hidden defects, electrical safety, structural integrity, ownership, or suitability for use.

## 2. Why this is a good small-VLM task

The task is narrow, repetitive, and structured. It is therefore suitable for a compact local model when the visual domain and output schema are controlled.

Potential operational uses include:

- workshop inventory checks;
- maintenance-kit completeness;
- tool-return verification;
- visual stock reconciliation;
- visible-condition triage;
- offline batch processing of workshop images.

The supplied small-VLM playbook uses the same general pattern: image-plus-instruction input, supervised fine-tuning, structured JSON output, hard negatives, and local demonstration. In this project, food categories are replaced with workshop tools and irrelevant scenes. The playbook also emphasises local processing, structured extraction, frozen-encoder experiments, and production scaling. fileciteturn300file1

## 3. Architecture

```text
Image
  ↓
Vision encoder
  ↓
Multimodal projector or connector
  ↓
Small language decoder
  ↓
Structured JSON tokens
```

A practical first experiment can freeze the vision encoder and train the connector and language-side components. This is an experimental strategy, not a universal rule. If the target images differ substantially from the original visual pretraining domain, later experiments may selectively unfreeze visual layers.

## 4. Dataset design

Recommended initial composition:

| Split | Purpose |
|---|---|
| Target-positive images | Tools, toolboxes, workshop benches, maintenance kits |
| Hard negatives | Office desks, kitchens, shelves, electronics, stationery, sports equipment |
| Difficult positives | Occlusion, glare, low light, clutter, partial views, similar-looking tools |
| Unanswerable images | Severe blur, crop, or obstruction requiring abstention |

Do not use a fixed positive-to-negative ratio without validation. Start with a meaningful hard-negative subset and tune the composition using false-positive results.

### Suggested tool classes

- hammer;
- screwdriver;
- adjustable wrench;
- spanner;
- pliers;
- socket wrench;
- sockets;
- drill;
- measuring tape;
- utility knife;
- hex keys;
- unknown tool.

### Annotation principles

- use a controlled vocabulary;
- annotate counts explicitly;
- use `unknown` when the visible evidence is insufficient;
- separate object identity from visible condition;
- document occlusion and image quality;
- avoid unsupported safety conclusions;
- include empty outputs for irrelevant scenes.

## 5. Conversational training format

A multimodal SFT record should contain a user message with an image and instruction, followed by an assistant message containing the exact target JSON.

```python
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "image": "images/workbench_001.jpg"},
            {
                "type": "text",
                "text": "Extract visible workshop tools into the required JSON schema.",
            },
        ],
    },
    {
        "role": "assistant",
        "content": [
            {"type": "text", "text": target_json},
        ],
    },
]
```

Current Hugging Face guidance supports VLM SFT datasets with `image` or `images` fields and conversational records. It also warns that sequence truncation can remove image tokens; verify token lengths before setting a maximum length.

## 6. Fine-tuning stages

### Stage A: baseline evaluation

Evaluate the base model before training:

- JSON parse rate;
- schema-validity rate;
- tool-name F1;
- count MAE;
- hard-negative false-positive rate;
- unsupported visual claims;
- latency and memory.

### Stage B: schema alignment

Fine-tune on carefully reviewed image-to-JSON examples. A reasonable initial experiment is:

- supervised fine-tuning;
- deterministic train/validation split by image source or capture session;
- assistant/completion-only loss where supported;
- vision encoder initially frozen;
- early stopping or checkpoint selection using validation schema accuracy;
- no final hyperparameter claims until experiments are run.

### Stage C: visual-domain adaptation

If the model confuses visually similar tools or fails under workshop-specific lighting, selectively unfreeze visual components or use parameter-efficient adaptation. Compare against the frozen-encoder baseline.

### Stage D: edge optimisation

After task quality is acceptable:

- export or convert the model for the intended runtime;
- test reduced precision or quantisation;
- measure memory, latency, throughput, and power;
- repeat task metrics after every optimisation step;
- test offline and failure-mode behaviour.

## 7. Evaluation design

| Metric | Purpose |
|---|---|
| JSON parse rate | Can the output be parsed? |
| Schema-validity rate | Does the output follow required keys and types? |
| Tool-name precision/recall/F1 | Are tools correctly included and omitted? |
| Count MAE | Are object quantities correct? |
| Hard-negative false-positive rate | Does the model invent tools in irrelevant scenes? |
| Condition accuracy | Are visible-condition labels correct? |
| Unsupported-claim rate | Does the model infer non-visible information? |
| Appropriate abstention | Does it reject unusable images? |
| Latency and peak memory | Can it run on the target edge device? |

Report base-model and fine-tuned-model results side by side. A valid JSON output is not sufficient if object recognition is wrong.

## 8. Public repository assets

```text
data/small_vlm_tool_inventory_examples.jsonl
src/learn_ai_evaluation/small_vlm_tool_inventory.py
examples/small-vlm-tool-inventory/tool_inventory_evaluation.py
tests/test_small_vlm_tool_inventory.py
```

Run:

```bash
python examples/small-vlm-tool-inventory/tool_inventory_evaluation.py
python -m pytest tests/test_small_vlm_tool_inventory.py -q
```

The JSONL file contains metadata and labels only. Replace the placeholder image paths with locally owned or properly licensed images before training.

## 9. Production cautions

- Do not claim “zero cost”; local inference still has hardware, energy, maintenance, and operational costs.
- Do not claim complete privacy solely because a model is local; access control, logging, storage, and update channels still matter.
- Do not treat training loss as evidence of deployment quality.
- Do not upload sensitive workshop imagery or proprietary equipment photos to public repositories.
- Do not use a visual condition label as a substitute for a competent safety inspection.
- Keep a held-out set representing real camera, lighting, background, and clutter conditions.

## 10. References

- Supplied *Small VLM Playbook* and strategic implementation document. fileciteturn300file0 fileciteturn300file1
- YouTube tutorial supplied by the user: https://www.youtube.com/watch?v=_EMfJSmLSKE
- Hugging Face TRL SFT Trainer: https://huggingface.co/docs/trl/sft_trainer
- Hugging Face image-text-to-text guide: https://huggingface.co/docs/transformers/main/en/tasks/image_text_to_text
- SmolVLM paper: https://arxiv.org/abs/2504.05299

## Key lesson

A small VLM can be useful when the task is narrow, the dataset is representative, the output schema is strict, and evaluation includes hard negatives, visual grounding, and edge constraints. Fine-tuning should be treated as a controlled engineering experiment rather than an assumption that a small model will automatically outperform a larger general model.
