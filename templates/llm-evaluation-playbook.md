# LLM Evaluation Playbook

## 1. Evaluation objective

- Application or workflow:
- User outcome that matters:
- Primary quality metric:
- Secondary metrics:
- Release decision owner:

## 2. Baseline and evaluation set

- Baseline source:
- Number of evaluation cases:
- Case selection method:
- Development set separated from test set: Yes / No
- Known coverage gaps:

## 3. Variants under comparison

| Variant | Prompt version | Model | Temperature | Other settings |
|---|---|---|---:|---|
|  |  |  |  |  |

## 4. Code-based checks

| Check | Rule | Result | Target | Status |
|---|---|---:|---:|---|
| Format validity |  |  |  |  |
| Required content |  |  |  |  |
| Forbidden content |  |  |  |  |
| Length |  |  |  |  |
| Task-specific metric |  |  |  |  |

## 5. Human evaluation

- Evaluation format: pairwise / rubric / pass-fail
- Reviewer expertise:
- Reviewer instructions:
- Number of calibration cases:
- Inter-reviewer agreement:

## 6. Model-based evaluator

- Evaluator model:
- Evaluator prompt version:
- Evaluation format:
- Human-alignment rate:
- Order-swapping used: Yes / No
- Known evaluator biases:

## 7. Results

| Variant | Raw win rate | Order-adjusted win rate | Human agreement | Quality score | Latency | Cost |
|---|---:|---:|---:|---:|---:|---:|
|  |  |  |  |  |  |  |

## 8. Failure analysis

Record major failure categories and representative examples.

## 9. Decision

- Selected variant:
- Reason:
- Remaining risks:
- Next evaluation date:
