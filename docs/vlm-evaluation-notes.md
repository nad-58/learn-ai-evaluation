# VLM Evaluation Notes: LVLM-eHub and VLMEvalKit

This note captures practical lessons for evaluating large vision-language models (VLMs/LVLMs). It is based on the LVLM-eHub paper and the open-source VLMEvalKit project.

## Why VLM evaluation needs a broad framework

VLMs should not be evaluated only with one captioning or VQA metric. A model can look strong on familiar benchmark tasks but behave differently in open-world visual question answering. Evaluation should therefore combine quantitative benchmark testing, hallucination checks, open-ended review, and where appropriate human preference assessment.

## Six capability groups from LVLM-eHub

A practical VLM evaluation plan should cover the following capability groups:

1. Visual perception: image classification, multi-class identification, object recognition, and object counting.
2. Visual knowledge acquisition: OCR, key information extraction, and image captioning.
3. Visual reasoning: VQA, knowledge-grounded image description, visual entailment, and spatial reasoning.
4. Visual commonsense: commonsense QA, visual commonsense reasoning, colour, shape, material, and composition reasoning.
5. Object hallucination: checking whether the answer mentions objects or visual details not present in the image.
6. Embodied or action-oriented intelligence: planning quality, object recognition in a scene, spatial understanding, reasonability, and executability.

## Evaluation methods

LVLM-eHub highlights four useful evaluation modes:

1. Question answering: ask a visual question and evaluate the answer with task-specific metrics.
2. Prefix-based scoring: for multiple-choice tasks, score candidate answers and select the best-supported option.
3. Multi-turn reasoning: decompose hard visual reasoning tasks into sub-questions, collect sub-answers, and combine them into a final judgement.
4. User or human study: use anonymised side-by-side comparison or rubric-based scoring where automated metrics are insufficient.

## Important risk areas

- In-domain overfitting: strong benchmark performance does not guarantee open-world generalisation.
- Object hallucination: the model may describe objects that are not in the image.
- Metric mismatch: captioning metrics such as CIDEr can fail when model answers are semantically acceptable but phrased differently.
- Prompt sensitivity: different prompt templates can change results.
- Long output and thinking-mode parsing: modern models may produce long reasoning traces or hidden-thinking style sections, which should be separated from final answers before scoring.

## Practical additions inspired by VLMEvalKit

VLMEvalKit is useful as a reference implementation because it supports many models and benchmarks through a common interface. Practical repository lessons include:

- use generation-based evaluation consistently across VLMs;
- support exact matching and LLM-based answer extraction;
- record model, prompt, dataset, and evaluator configuration;
- separate final answer text from long reasoning traces when needed;
- store long predictions in a format that avoids truncation;
- allow custom model wrappers and custom benchmark adapters;
- document dependency versions because some VLMs require specific transformers or vision-library versions.

## Recommended repository checklist

For each VLM evaluation experiment, record:

- model name and version;
- visual encoder or model family if known;
- prompt template;
- dataset and task category;
- image source and number of samples;
- expected answer or expected visual concepts;
- generated answer;
- answer extraction method;
- scoring method;
- hallucination flags;
- human review notes where relevant;
- limitations and failure cases.

## Suggested metrics

| Capability | Example metrics |
|---|---|
| Visual perception | accuracy, object recall, counting error |
| OCR and document understanding | word accuracy, entity-level F1, extraction accuracy |
| VQA and reasoning | exact match, accuracy, MRR, human rubric score |
| Captioning | CIDEr, semantic similarity, human quality score |
| Hallucination | yes-ratio, precision, recall, F1, unsupported-object count |
| Open-world comparison | pairwise preference, win rate, Elo-style ranking |
| Embodied planning | object recognition score, spatial score, reasonability, executability |

## How to use this note

Use this file together with:

```text
tutorials/007-advanced-ai-evaluation/README.md
templates/vlm-evaluation-report.md
examples/advanced-ai-evaluation/advanced_ai_evaluation_example.py
```
