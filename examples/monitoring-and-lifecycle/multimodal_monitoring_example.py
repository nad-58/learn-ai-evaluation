"""Numerical monitoring example for tabular, image, and speech data."""
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from learn_ai_evaluation.monitoring_lifecycle import feature_drift_report
from learn_ai_evaluation.multimodal_monitoring import (
    audio_summary_features,
    compare_feature_sets,
    image_summary_features,
)

DATA = ROOT / "data" / "monitoring"


def main() -> None:
    tabular_reference = pd.read_csv(DATA / "tabular_reference.csv")
    tabular_current = pd.read_csv(DATA / "tabular_current.csv")
    tabular_drift = feature_drift_report(
        tabular_reference,
        tabular_current,
        ["age", "score", "latency_ms"],
        bins=4,
    )

    image_reference = pd.read_csv(DATA / "image_reference.csv").drop(columns="row")
    image_current = pd.read_csv(DATA / "image_current.csv").drop(columns="row")
    image_reference_features = image_summary_features(image_reference.to_numpy())
    image_current_features = image_summary_features(image_current.to_numpy())
    image_comparison = pd.DataFrame(
        compare_feature_sets(image_reference_features, image_current_features)
    )

    speech_reference = pd.read_csv(DATA / "speech_reference.csv")["amplitude"]
    speech_current = pd.read_csv(DATA / "speech_current.csv")["amplitude"]
    speech_reference_features = audio_summary_features(speech_reference, sample_rate=8000)
    speech_current_features = audio_summary_features(speech_current, sample_rate=8000)
    speech_comparison = pd.DataFrame(
        compare_feature_sets(speech_reference_features, speech_current_features)
    )

    print("TABULAR DATA DRIFT")
    print(tabular_drift.round(4).to_string(index=False))

    print("\nIMAGE FEATURE CHANGE")
    print(image_comparison.round(4).to_string(index=False))

    print("\nSPEECH FEATURE CHANGE")
    print(speech_comparison.round(4).to_string(index=False))

    print("\nINTERPRETATION")
    print("- Tabular monitoring detects shifts in age, score, and latency.")
    print("- Image monitoring detects increased brightness and changed edge statistics.")
    print("- Speech monitoring detects reduced amplitude and a dominant-frequency shift.")
    print("- These are screening signals; model performance and operational context must also be reviewed.")


if __name__ == "__main__":
    main()
