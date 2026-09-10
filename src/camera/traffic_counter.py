"""MediaPipe-based traffic detection for person, bicycle and car classes."""
import argparse
import json
import time
from pathlib import Path

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from picamera2 import Picamera2

TARGETS = {"person": "person_count", "bicycle": "bicycle_count", "car": "car_count"}

def write_counts(path, station_id, counts):
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"type": "measure", "id": station_id, "time": int(time.time()), "readings": counts}
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--output", default="runtime/latest_counts.json")
    parser.add_argument("--station-id", type=int, default=101)
    parser.add_argument("--score-threshold", type=float, default=0.5)
    parser.add_argument("--interval", type=float, default=1.0)
    args = parser.parse_args()

    options = vision.ObjectDetectorOptions(
        base_options=python.BaseOptions(model_asset_path=args.model),
        score_threshold=args.score_threshold,
        max_results=20)
    detector = vision.ObjectDetector.create_from_options(options)
    camera = Picamera2()
    camera.configure(camera.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
    camera.start()
    output = Path(args.output)
    counts = {"person_count": 0, "bicycle_count": 0, "car_count": 0}
    print("AP9 camera detection started.")
    print("Mode: cumulative counter")
    print("Stop with CTRL+C")
    try:
        while True:
            frame = camera.capture_array()
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            result = detector.detect(image)
            for detection in result.detections:
                if not detection.categories:
                    continue
                metric = TARGETS.get(detection.categories[0].category_name)
                if metric:
                    counts[metric] = min(255, counts[metric] + 1)
            write_counts(output, args.station_id, counts)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        pass
    finally:
        camera.stop()
        detector.close()

if __name__ == "__main__":
    main()
