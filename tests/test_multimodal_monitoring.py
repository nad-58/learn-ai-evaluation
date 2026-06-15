import numpy as np
import pytest

from learn_ai_evaluation.multimodal_monitoring import (
    audio_summary_features,
    compare_feature_sets,
    image_summary_features,
)


def test_image_summary_features():
    image = np.array([[0.0, 0.5], [0.5, 1.0]])
    features = image_summary_features(image)
    assert features["mean_intensity"] == pytest.approx(0.5)
    assert features["minimum_intensity"] == 0.0
    assert features["maximum_intensity"] == 1.0
    assert features["bright_pixel_rate"] == pytest.approx(0.25)
    assert features["mean_edge_magnitude"] == pytest.approx(0.5)


def test_audio_summary_features_detect_frequency_and_amplitude():
    reference = [0.0, 0.7071, 1.0, 0.7071, 0.0, -0.7071, -1.0, -0.7071] * 4
    current = [0.0, 0.7, 0.0, -0.7] * 8
    reference_features = audio_summary_features(reference, sample_rate=8000)
    current_features = audio_summary_features(current, sample_rate=8000)

    assert reference_features["dominant_frequency_hz"] == pytest.approx(1000.0)
    assert current_features["dominant_frequency_hz"] == pytest.approx(2000.0)
    assert current_features["rms_amplitude"] < reference_features["rms_amplitude"]


def test_compare_feature_sets():
    rows = compare_feature_sets(
        {"mean": 2.0, "std": 1.0},
        {"mean": 3.0, "std": 0.5},
    )
    by_name = {row["feature"]: row for row in rows}
    assert by_name["mean"]["absolute_change"] == pytest.approx(1.0)
    assert by_name["mean"]["relative_change"] == pytest.approx(0.5)
    assert by_name["std"]["relative_change"] == pytest.approx(-0.5)
