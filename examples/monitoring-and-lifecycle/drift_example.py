from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.monitoring_lifecycle import feature_drift_report

reference = pd.DataFrame({
    "age": [22, 25, 31, 38, 41, 52, 63, 70, 29, 34],
    "score": [0.42, 0.55, 0.61, 0.67, 0.72, 0.78, 0.84, 0.91, 0.58, 0.64],
})
current = pd.DataFrame({
    "age": [35, 39, 44, 48, 53, 59, 66, 72, 46, 51],
    "score": [0.38, 0.49, 0.54, 0.60, 0.65, 0.70, 0.76, 0.82, 0.57, 0.62],
})

print(feature_drift_report(reference, current, ["age", "score"], bins=5).round(4).to_string(index=False))
