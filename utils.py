import base64
import cv2
import numpy as np


def decode_image_bytes(data: bytes):
    array = np.frombuffer(data, dtype=np.uint8)
    return cv2.imdecode(array, cv2.IMREAD_COLOR)


def encode_jpeg(frame, quality=88):
    ok, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not ok:
        raise ValueError("Could not encode image")
    return base64.b64encode(buffer).decode("ascii")
