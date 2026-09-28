import cv2


def process_video(input_path, output_path, detector, max_frames=600):
    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        raise RuntimeError("Could not open video")

    fps = cap.get(cv2.CAP_PROP_FPS) or 20.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)

    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    summary = {"frames": 0, "critical": 0, "warning": 0, "fire": 0, "smoke": 0}

    while summary["frames"] < max_frames:
        ok, frame = cap.read()
        if not ok:
            break
        result = detector.analyze(frame)
        writer.write(detector.draw(frame, result))
        summary["frames"] += 1
        summary["critical"] += int(result["status"] == "CRITICAL")
        summary["warning"] += int(result["status"] == "WARNING")
        summary["fire"] += int(result["fire_detected"])
        summary["smoke"] += int(result["smoke_detected"])

    cap.release()
    writer.release()
    return summary
