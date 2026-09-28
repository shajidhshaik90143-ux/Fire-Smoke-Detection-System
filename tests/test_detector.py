import numpy as np
import cv2
from detector import FireSmokeDetector


def test_detector_returns_expected_keys():
    result = FireSmokeDetector().analyze(np.zeros((480, 640, 3), dtype=np.uint8))
    assert result["status"] in {"SAFE", "WARNING", "CRITICAL"}
    assert "fire_score" in result
    assert "smoke_score" in result
    assert isinstance(result["detections"], list)


def test_fire_like_patch_runs():
    image = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.rectangle(image, (220, 150), (420, 350), (0, 80, 255), -1)
    result = FireSmokeDetector().analyze(image)
    assert result["fire_score"] >= 0.0
