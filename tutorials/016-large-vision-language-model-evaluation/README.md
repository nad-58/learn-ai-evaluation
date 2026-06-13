# Large Vision-Language Model Evaluation

Large vision-language models combine visual inputs and language understanding or generation. They are different from both **large language models** and **large vision models**.

- A large language model operates primarily over text or token sequences.
- A large vision model operates primarily over images or video and produces visual features, labels, boxes, masks, or other perception outputs.
- A vision-language model explicitly connects visual and linguistic representations.
- A vision-language-action model extends this connection into action generation or control.

See [`docs/llm-lvm-vlm-vla-taxonomy.md`](../../docs/llm-lvm-vlm-vla-taxonomy.md) before selecting evaluation metrics.

A VLM can take several architectural forms. CLIP-like systems align image and text embeddings, while generative multimodal assistants combine visual encoders with language models and generate text. These systems belong to the same broad family but require different evaluation methods.

Their evaluation therefore needs to test more than text quality or overall benchmark accuracy.

A complete evaluation should cover:

- task correctness;
- visual perception;
- cross-modal grounding;
- hallucination and unsupported claims;
- answerability and abstention;
- retrieval and localisation;
- robustness across image and prompt variation;
- group and slice performance;
- safety, efficiency, and system behaviour.

All examples in this chapter are synthetic and public-safe.

## 1. Define the intended task

Metrics must match the task. Typical task families include visual question answering, image captioning, image-text retrieval, OCR, document understanding, multimodal classification, grounding, multi-image reasoning, and tool-assisted workflows.

Do not combine unrelated tasks into one headline score. Define the input, output, unit of analysis, expected use, and important failure modes before choosing metrics.

## 2. Separate perception, reasoning, and generation

A wrong answer may occur because the model failed to recognise the visual content, linked the wrong visual evidence to the prompt, reasoned incorrectly, or generated an unsupported answer.

```text
Visual perception
      ↓
Cross-modal alignment
      ↓
Reasoning
      ↓
Answer generation
      ↓
Integrated system output
```

Report capability-level results for object recognition, counting, colour, spatial relationships, actions, OCR, charts, diagrams, document structure, knowledge, and multi-image understanding.

## 3. Task metrics

For short-answer visual question answering:

```text
Exact Match = 1 when normalized reference equals normalized prediction
```

```text
Precision = overlapping tokens / predicted tokens
Recall    = overlapping tokens / reference tokens
F1        = 2 × Precision × Recall / (Precision + Recall)
```

For image-text retrieval:

```text
Recall@K = queries with a relevant item in the top K / all queries
MRR      = mean of 1 / rank of the first relevant item
```

For grounding or localisation, use measures such as intersection over union, pointing accuracy, region accuracy, or claim-to-region verification where suitable.

## 4. Grounding and unsupported claims

Fluent output is not evidence that the model used the image correctly. Evaluate whether each generated visual claim is supported by visible evidence.

```text
Unsupported Claim Rate
= outputs containing unsupported visual claims / reviewed outputs
```

For detailed review:

```text
Claim Grounding Precision
= visually supported claims / all generated visual claims
```

Useful failure labels include invented object, incorrect attribute, incorrect count, incorrect spatial relationship, incorrect text reading, contradiction, and unsupported inference.

## 5. Answerability and abstention

Include examples that cannot be answered from the available image. These may contain missing evidence, severe blur, crop, occlusion, ambiguity, or an absent image.

```text
Appropriate Abstention Rate
= abstentions on unanswerable inputs / unanswerable inputs
```

```text
Unnecessary Abstention Rate
= abstentions on answerable inputs / answerable inputs
```

This prevents a model from being rewarded for confident guessing or excessive refusal.

## 6. Caption and open-ended generation

Open-ended outputs should combine automated and human evaluation. Useful dimensions include semantic correctness, object coverage, attribute accuracy, relation accuracy, relevance, completeness, usefulness, and unsupported claims.

Lexical overlap alone is insufficient because several different captions can correctly describe the same image.

## 7. Group and slice analysis

Overall averages can hide important weaknesses. Report performance with sample counts across relevant slices, such as:

- image resolution, lighting, blur, crop, compression, and occlusion;
- common and rare objects;
- question type and complexity;
- OCR, counting, spatial, action, and reasoning tasks;
- prompt language and style;
- source, acquisition environment, or device where relevant;
- single-image and multi-image inputs.

Small groups should be reported with uncertainty and interpreted cautiously.

## 8. Robustness

Test controlled changes to both modalities.

Visual changes may include noise, blur, compression, contrast, brightness, resizing, occlusion, or irrelevant visual regions. Language changes may include paraphrasing, spelling errors, distractor text, prompt order, and conflicting instructions.

```text
Relative Performance Drop
= (baseline score - perturbed score) / baseline score
```

Confirm that a perturbation preserves the expected answer before treating a score change as a robustness failure.

## 9. Human and model-based judging

Open-ended evaluation requires a clear rubric. Score correctness, visual grounding, completeness, relevance, clarity, and uncertainty separately.

Document the judge, prompt, rubric, examples, randomisation, reviewer competence, conflict resolution, and agreement checks. Model-based judging should not be the only evidence for important conclusions.

## 10. Safety and adversarial evaluation

Test multimodal risks including text embedded in images, conflicting image and prompt instructions, hidden instructions in documents, privacy-sensitive visual content, unsafe inferences, harmful content, prompt injection, and excessive refusal of benign tasks.

## 11. Efficiency and operational behaviour

Record latency, throughput, memory, token usage, cost, failed requests, invalid file handling, supported image formats, image-count limits, and behaviour when images are missing or reordered.

## 12. System-level evaluation

A deployed application may include preprocessing, OCR, retrieval, prompt construction, model inference, tool calls, output parsing, and user-interface logic.

Evaluate the integrated pipeline, including fallback behaviour, logging, recovery, monitoring, and human escalation. Model-only benchmark results do not establish system reliability.

## 13. Reproducibility

Record model and checkpoint identifiers, provider, prompt template, system instructions, image preprocessing, resolution, decoding settings, image order, dataset version, split method, metric implementation, judge configuration, software environment, evaluation date, exclusions, and known limitations.

Use `templates/vlm-evaluation-report-template.md` for structured reporting.

## 14. Run the example

```bash
python examples/vlm-evaluation/basic_vlm_evaluation_example.py
```

The example demonstrates exact match, token F1, Recall@K, mean reciprocal rank, unsupported-claim rate, and abstention metrics using synthetic data.

## Key lesson

A vision-language model should not be judged only by whether its response sounds plausible. Evaluation must establish whether the output is correct, visually grounded, robust, appropriately uncertain, safe, efficient, and reliable after integration into the wider system.
