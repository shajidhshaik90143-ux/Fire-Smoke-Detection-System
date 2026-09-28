from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
from datetime import datetime

from config import (
    UPLOAD_DIR, ALERT_DIR, MAX_CONTENT_LENGTH,
    ALLOWED_IMAGE_EXTENSIONS, ALLOWED_VIDEO_EXTENSIONS
)
from detector import FireSmokeDetector
from alerts import record_event
from utils import decode_image_bytes, encode_jpeg
from camera import process_video

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
detector = FireSmokeDetector()


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "service": "Fire & Smoke Detection System"})


@app.post("/api/analyze")
def analyze():
    uploaded = request.files.get("file")
    if not uploaded or not uploaded.filename:
        return jsonify({"error": "Please upload an image"}), 400

    suffix = Path(uploaded.filename).suffix.lower()
    if suffix not in ALLOWED_IMAGE_EXTENSIONS:
        return jsonify({"error": "Unsupported image type"}), 400

    frame = decode_image_bytes(uploaded.read())
    if frame is None:
        return jsonify({"error": "Invalid image"}), 400

    result = detector.analyze(frame)
    annotated = detector.draw(frame, result)
    snapshot = record_event(ALERT_DIR, result, annotated)

    return jsonify({**result, "snapshot": snapshot, "image": encode_jpeg(annotated)})


@app.post("/api/frame")
def frame():
    uploaded = request.files.get("frame")
    if not uploaded:
        return jsonify({"error": "Missing frame"}), 400

    image = decode_image_bytes(uploaded.read())
    if image is None:
        return jsonify({"error": "Invalid frame"}), 400

    result = detector.analyze(image)
    annotated = detector.draw(image, result)

    if result["status"] in {"WARNING", "CRITICAL"}:
        record_event(ALERT_DIR, result, annotated)

    return jsonify({**result, "image": encode_jpeg(annotated, 82)})


@app.post("/api/video")
def video():
    uploaded = request.files.get("file")
    if not uploaded or not uploaded.filename:
        return jsonify({"error": "Please upload a video"}), 400

    suffix = Path(uploaded.filename).suffix.lower()
    if suffix not in ALLOWED_VIDEO_EXTENSIONS:
        return jsonify({"error": "Unsupported video type"}), 400

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    input_path = UPLOAD_DIR / f"input_{stamp}{suffix}"
    output_path = UPLOAD_DIR / f"processed_{stamp}.mp4"
    uploaded.save(input_path)

    summary = process_video(input_path, output_path, detector)
    return jsonify({"summary": summary, "processed_video": output_path.name})


@app.get("/uploads/<path:filename>")
def uploads(filename):
    return send_from_directory(UPLOAD_DIR, filename)


@app.get("/alerts/<path:filename>")
def alerts(filename):
    return send_from_directory(ALERT_DIR, filename)


if __name__ == "__main__":
    print("Fire & Smoke Detection System")
    print("Open http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
