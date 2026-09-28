# Fire & Smoke Detection System

A portfolio-ready computer-vision project for detecting fire-like and smoke-like regions from uploaded images, videos, and live webcam frames.

## Features
- Real-time browser webcam monitoring
- Image upload analysis
- Video-file processing
- Fire detection using HSV/color segmentation, morphology and contours
- Smoke detection using saturation, brightness and texture heuristics
- SAFE / WARNING / CRITICAL status
- Detection boxes and confidence-like scores
- Alert snapshots and CSV event log
- Flask web dashboard
- JSON API endpoints
- Modular detector ready for future YOLO/custom-model integration
- No external model download required for the baseline

> Educational/early-warning prototype only. It must not replace certified fire alarms or emergency systems.

## Recommended Python
Python 3.11 or 3.12 is recommended.

## Install and Run (Windows PowerShell)
```powershell
cd Fire_Smoke_Detection_System
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Run with one command
Double-click `run.bat`.

## API
- `GET /api/health`
- `POST /api/analyze` with multipart field `file`
- `POST /api/frame` with multipart field `frame`
- `POST /api/video` with multipart field `file`

## Project Structure
```text
Fire_Smoke_Detection_System/
├── app.py
├── config.py
├── detector.py
├── camera.py
├── alerts.py
├── utils.py
├── requirements.txt
├── PROJECT_REPORT.md
├── run.bat
├── templates/index.html
├── static/style.css
├── static/app.js
├── tests/test_detector.py
├── models/README.md
└── data/
    ├── uploads/
    └── alerts/
```

## Detection
Fire uses warm-color response, HSV saturation/value thresholds, morphology and contour analysis.
Smoke uses low saturation, brightness and soft/local-texture characteristics.

Scores are heuristic confidence-like values, not calibrated probabilities.

## Future upgrades
- YOLO fire/smoke object detection
- Custom dataset training and evaluation
- CCTV/IP camera support
- Firebase/Telegram/email/SMS notifications
- Multi-camera dashboard
- Temporal tracking and false-positive suppression
- Raspberry Pi / Jetson deployment
- Precision, recall, mAP and FPS evaluation

## Safety
Do not use this application as the sole safety mechanism in a real building. Use certified fire/smoke alarms and follow local emergency procedures.
