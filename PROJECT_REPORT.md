# Fire & Smoke Detection System — Project Report

## Abstract
This project implements a computer-vision early-warning prototype for visual fire and smoke detection. A Flask backend receives images, video and webcam frames. OpenCV performs color segmentation, morphology, contour analysis and grayscale texture analysis. Results are displayed in a browser dashboard and alert snapshots are logged.

## Objectives
1. Detect fire-like visual regions.
2. Detect smoke-like visual regions.
3. Provide real-time camera analysis.
4. Generate warning and critical states.
5. Save alert evidence.
6. Provide an extensible platform for deep-learning models.

## Modules
- Dashboard
- Live camera
- Image analyzer
- Video processor
- Fire detector
- Smoke detector
- Alert logger
- REST API

## Technologies
Python, Flask, OpenCV, NumPy, HTML, CSS and JavaScript.

## Future Scope
Use a labeled fire/smoke dataset and a modern object detector, then evaluate precision, recall, mAP, FPS and false alarms across day/night and indoor/outdoor scenes. Add CCTV/IP streams, notifications, multi-camera support and edge deployment.

## Limitations
Visual fire/smoke detection is affected by lighting, orange objects, gray surfaces, steam, dust, clouds, compression and camera angle. The included scores are heuristic confidence-like values, not calibrated probabilities.

## Safety
This is an educational prototype and must not replace certified fire alarms, smoke detectors or emergency procedures.
