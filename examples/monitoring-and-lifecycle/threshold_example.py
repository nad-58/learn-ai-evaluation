from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.monitoring_lifecycle import ThresholdRule, evaluate_threshold_rules, lifecycle_decision

metrics = {"auroc": 0.81, "recall": 0.69, "precision": 0.74}
rules = [
    ThresholdRule("auroc", warning=0.82, action=0.78),
    ThresholdRule("recall", warning=0.72, action=0.68),
    ThresholdRule("precision", warning=0.70, action=0.65),
]
checks = evaluate_threshold_rules(metrics, rules)
print(pd.Series(metrics).to_string())
print(checks.to_string(index=False))
print(lifecycle_decision(checks))
