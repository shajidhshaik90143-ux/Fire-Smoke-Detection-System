# Optional Models

The baseline system works without model weights.

For a stronger research/production-oriented version, place a trained fire/smoke object-detection model here and add a model adapter in `detector.py`.

Suggested classes:
- fire
- smoke

Evaluate any model using precision, recall, mAP and FPS on data representative of the intended camera environment.
