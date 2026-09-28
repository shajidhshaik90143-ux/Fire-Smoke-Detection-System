import csv
from datetime import datetime
from pathlib import Path
import cv2


def ensure_log(path: Path):
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                "timestamp", "status", "fire_detected", "smoke_detected",
                "fire_score", "smoke_score", "snapshot"
            ])


def record_event(alert_dir: Path, result: dict, frame=None):
    alert_dir.mkdir(parents=True, exist_ok=True)
    log_path = alert_dir / "events.csv"
    ensure_log(log_path)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    snapshot_name = ""

    if result["status"] in {"WARNING", "CRITICAL"} and frame is not None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        snapshot_name = f"alert_{stamp}.jpg"
        cv2.imwrite(str(alert_dir / snapshot_name), frame)

    with log_path.open("a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            timestamp, result["status"], result["fire_detected"],
            result["smoke_detected"], result["fire_score"],
            result["smoke_score"], snapshot_name
        ])
    return snapshot_name
