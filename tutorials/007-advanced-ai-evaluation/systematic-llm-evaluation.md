# Systematic LLM Evaluation: Beyond the Vibe Check

A vibe check means manually skimming individual outputs and deciding whether they feel acceptable. This is useful during early prototyping because it supports fast learning, rapid prompt changes, and creation of an initial baseline. It becomes unreliable when a system must compare many prompts, models, temperatures, examples, or releases.

Systematic evaluation converts subjective impressions into repeatable measurements that correlate with outcomes the project actually values.

## When to move beyond a vibe check

Move from manual inspection to a programmatic evaluation pipeline when:

- more than one model or prompt version must be compared;
- changes need to be versioned and reproduced;
- the same test set must be rerun after updates;
- user outcomes differ from developer impressions;
- latency, cost, safety, and output quality must be reviewed together;
- the application is moving from prototype to production.

## The three evaluation pillars

### 1. Code-based evaluation

Code-based evaluation is appropriate for objective or structural requirements.

Examples:

- exact match and test-case execution;
- JSON-schema validation;
- title or response length;
- required and forbidden phrases;
- regex and string checks;
- task-specific accuracy;
- BLEU or ROUGE where similarity is a meaningful proxy.

Advantages include speed, low cost, reproducibility, and suitability for continuous integration. The main limitation is rigidity: code checks often fail to capture quality, style, empathy, usefulness, or nuanced factuality.

### 2. Human-based evaluation

Human evaluation is the strongest source of truth for taste, tone, empathy, domain judgement, and open-ended quality.

Two useful formats are:

- pairwise preference: compare two outputs and select the better response;
- rubric grading: score one response against explicit quality criteria.

Human evaluation is valuable because it forces the team to define what a good output means. It is also slow and expensive, so it is best used to create a representative calibration set rather than grade every production output.

### 3. Model-based evaluation

A model-based evaluator can apply a human-defined rubric at scale. It is useful for pairwise comparison, pass/fail grading, multi-dimensional scoring, and failure categorisation.

A model-based evaluator should not be trusted before calibration. Its labels should be compared against human labels on a representative set, and disagreement cases should be reviewed.

## Evaluator risks and mitigations

### Order bias

An evaluator may prefer the first response shown. Evaluate the same pair in both orders and average the win rates.

### Self-preference and model-family bias

An evaluator may favour outputs that resemble its own style. Use human calibration, more than one evaluator where practical, and disagreement analysis.

### Weak or ambiguous rubrics

A vague rubric produces unstable labels. Define dimensions, scoring anchors, failure categories, and examples before scaling evaluation.

### Proxy-metric failure

A similarity metric may improve while the outcome users care about declines. Track both proxy metrics and the primary quality measure, and flag movement in opposite directions.

## Five-step evaluation blueprint

### Step 1: Curate a baseline

Create a representative set of high-quality examples, accepted outputs, human-written references, or expert-labelled cases. Record why each example is considered acceptable.

### Step 2: Prepare evaluation inputs

Collect the source prompts, documents, conversations, transcripts, or task inputs associated with the baseline. Remove duplicates and separate development examples from final evaluation cases.

### Step 3: Generate a starting system output

Run the initial prompt and model configuration on the full evaluation set. Store the prompt version, model version, temperature, seed where available, latency, token usage, and cost.

### Step 4: Calibrate the evaluator

Ask humans to label a representative subset. Run the automated evaluator on the same cases and calculate agreement. Review disagreement examples and refine the rubric until the evaluator is sufficiently aligned for the intended use.

### Step 5: Iterate and optimise

Compare each candidate prompt or system version with the baseline. Track win rate, rubric dimensions, rule-based checks, latency, and cost. Retain results for every version so regressions remain visible.

## Recommended experiment record

For every evaluation run, store:

- experiment and dataset version;
- prompt and model version;
- generation parameters;
- baseline and candidate outputs;
- rule-based metrics;
- evaluator labels and reasoning summaries;
- human labels for calibration cases;
- agreement rate;
- order-adjusted win rate;
- latency and estimated cost;
- known limitations and release decision.

## Repository implementation

Utilities:

```text
src/learn_ai_evaluation/llm_judge.py
```

Worked example:

```bash
python examples/llm-judge-evaluation/llm_judge_example.py
```

Templates:

```text
templates/llm-evaluation-playbook.md
templates/llm-evaluator-alignment.md
templates/prompt-iteration-report.md
```

Tests:

```bash
python -m pytest tests/test_llm_judge.py -q
```

## Practical principle

Use vibe checks to learn what should be measured. Use humans to define and validate quality. Use code and calibrated model-based evaluators to scale the resulting evaluation process.
