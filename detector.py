import cv2
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class Detection:
    label: str
    score: float
    bbox: Tuple[int, int, int, int]
    area_ratio: float


class FireSmokeDetector:
    """Explainable baseline fire/smoke computer-vision detector."""

    def __init__(self, min_area_ratio: float = 0.002):
        self.min_area_ratio = min_area_ratio

    @staticmethod
    def _normalize(v: float, lo: float, hi: float) -> float:
        if hi <= lo:
            return 0.0
        return float(np.clip((v - lo) / (hi - lo), 0.0, 1.0))

    def _fire_mask(self, frame: np.ndarray) -> np.ndarray:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        b, g, r = cv2.split(frame)

        red_dominance = (r.astype(np.int16) - g.astype(np.int16)) > 25
        warm = (r.astype(np.int16) > 120) & (g.astype(np.int16) > 55)
        yellow_orange = (
            (g.astype(np.int16) > 45) &
            (r.astype(np.int16) > g.astype(np.int16) + 15)
        )
        sat = hsv[:, :, 1]
        val = hsv[:, :, 2]

        mask = (red_dominance | yellow_orange) & warm & (sat > 80) & (val > 130)
        mask = mask.astype(np.uint8) * 255

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        _, mask = cv2.threshold(mask, 80, 255, cv2.THRESH_BINARY)
        return mask

    def _smoke_mask(self, frame: np.ndarray) -> np.ndarray:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        sat = hsv[:, :, 1]
        val = hsv[:, :, 2]
        low_sat = sat < 75
        useful_brightness = (val > 55) & (val < 235)

        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        diff = cv2.absdiff(gray, blur)
        soft = diff < 28

        mask = low_sat & useful_brightness & soft
        mask = mask.astype(np.uint8) * 255

        kernel = np.ones((9, 9), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.GaussianBlur(mask, (7, 7), 0)
        _, mask = cv2.threshold(mask, 90, 255, cv2.THRESH_BINARY)
        return mask

    def _regions(self, mask: np.ndarray, label: str, frame_shape) -> List[Detection]:
        h, w = frame_shape[:2]
        total = float(h * w)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        results = []

        for contour in contours:
            area = cv2.contourArea(contour)
            ratio = area / total
            if ratio < self.min_area_ratio:
                continue

            x, y, bw, bh = cv2.boundingRect(contour)
            fill = area / max(float(bw * bh), 1.0)
            size_score = self._normalize(ratio, self.min_area_ratio, 0.15)
            fill_score = float(np.clip(fill, 0.0, 1.0))
            score = float(np.clip(0.55 * size_score + 0.45 * fill_score, 0.0, 1.0))

            results.append(Detection(label, score, (x, y, bw, bh), ratio))

        results.sort(key=lambda d: d.score, reverse=True)
        return results[:8]

    def analyze(self, frame: np.ndarray) -> Dict:
        if frame is None or frame.size == 0:
            raise ValueError("Invalid image/frame")

        fire = self._regions(self._fire_mask(frame), "FIRE", frame.shape)
        smoke = self._regions(self._smoke_mask(frame), "SMOKE", frame.shape)

        fire_score = max((d.score for d in fire), default=0.0)
        smoke_score = max((d.score for d in smoke), default=0.0)

        fire_strong = [d for d in fire if d.score >= 0.32]
        smoke_strong = [d for d in smoke if d.score >= 0.30]

        if fire_score >= 0.65 or len(fire_strong) >= 2:
            status = "CRITICAL"
        elif fire_score >= 0.32 or smoke_score >= 0.45:
            status = "WARNING"
        else:
            status = "SAFE"

        detections = fire + smoke
        return {
            "status": status,
            "fire_detected": bool(fire_strong),
            "smoke_detected": bool(smoke_strong),
            "fire_score": round(float(fire_score), 3),
            "smoke_score": round(float(smoke_score), 3),
            "detections": [
                {
                    "label": d.label,
                    "score": round(float(d.score), 3),
                    "bbox": list(d.bbox),
                    "area_ratio": round(float(d.area_ratio), 5),
                }
                for d in detections
            ],
        }

    def draw(self, frame: np.ndarray, result: Dict) -> np.ndarray:
        output = frame.copy()
        for d in result["detections"]:
            x, y, w, h = d["bbox"]
            label = d["label"]
            score = d["score"]
            color = (0, 0, 255) if label == "FIRE" else (180, 180, 180)
            cv2.rectangle(output, (x, y), (x + w, y + h), color, 2)
            text = f"{label} {score:.2f}"
            cv2.rectangle(output, (x, max(0, y - 28)),
                          (x + max(130, w), y), color, -1)
            cv2.putText(output, text, (x + 5, max(18, y - 7)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                        (255, 255, 255), 2, cv2.LINE_AA)

        cv2.rectangle(output, (10, 10), (280, 50), (30, 30, 30), -1)
        cv2.putText(output, f"STATUS: {result['status']}", (20, 38),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                    (255, 255, 255), 2, cv2.LINE_AA)
        return output
