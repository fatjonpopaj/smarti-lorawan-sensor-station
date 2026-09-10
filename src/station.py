"""Main process for the Smarti Raspberry Pi LoRaWAN sensor station."""
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC))

from lorawan.lora_client import LoRaClient
from lorawan.payload_encoder import encode_login, encode_measure
from sensors.bme280_reader import BME280Reader
from sensors.gps_reader import GPSReader
from sensors.line_tracker import LineTracker
from sensors.sds011_reader import SDS011Reader

MEASURE_INTERVAL_SECONDS = 30
CAMERA_MAX_AGE_SECONDS = 10

def load_config():
    path = Path(os.getenv("SMARTI_CONFIG", str(ROOT / "config" / "station_config.json")))
    if not path.exists():
        raise FileNotFoundError("Copy config/station_config.example.json to config/station_config.json first.")
    return json.loads(path.read_text(encoding="utf-8"))

def read_camera_counts():
    path = Path(os.getenv("CAMERA_COUNTS_PATH", "/home/pi/ap9_mediapipe/latest_counts.json"))
    if not path.exists():
        raise RuntimeError("Keine aktuelle AP9-Kamera-Datei gefunden")
    age = time.time() - path.stat().st_mtime
    if age > CAMERA_MAX_AGE_SECONDS:
        raise RuntimeError(f"AP9-Kameradaten sind nicht live genug. Datei ist {age:.1f}s alt")
    data = json.loads(path.read_text(encoding="utf-8"))
    readings = data.get("readings", data)
    return (int(readings.get("person_count", 0)),
            int(readings.get("bicycle_count", 0)),
            int(readings.get("car_count", 0)))

def require_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required environment variable is missing: {name}")
    return value

def main():
    config = load_config()
    station_id = int(config["station_id"])
    lora = LoRaClient(require_env("LORA_PORT"), int(os.getenv("LORA_BAUD", "9600")))
    gps = GPSReader(require_env("GPS_PORT"), int(os.getenv("GPS_BAUD", "9600")))
    sds011 = SDS011Reader(require_env("SDS011_PORT"), int(os.getenv("SDS011_BAUD", "9600")))
    env = BME280Reader(int(os.getenv("BME280_BUS", "1")), int(os.getenv("BME280_ADDRESS", "0x76"), 0))
    line = LineTracker(int(os.getenv("LINE_TRACKER_GPIO", "17")))
    try:
        print(f"Station {station_id}: waiting for GPS fix...")
        latitude, longitude = gps.wait_for_fix(60)
        print("Joining LoRaWAN...")
        print(lora.join())
        print("Sending login...")
        print(lora.send_hex(encode_login(station_id, latitude, longitude)))
        while True:
            started = time.monotonic()
            try:
                temperature, humidity = env.read()
                pm25, pm10 = sds011.read()
                line_value = line.read()
                person_count, bicycle_count, car_count = read_camera_counts()
                batt = 99
                payload = encode_measure(
                    station_id, pm25=pm25, pm10=pm10, temperature=temperature,
                    humidity=humidity, line_tracker=line_value,
                    person_count=person_count, bicycle_count=bicycle_count,
                    car_count=car_count, batt=batt)
                print({"pm25": pm25, "pm10": pm10, "temperature": temperature,
                       "humidity": humidity, "line_tracker": line_value,
                       "person_count": person_count, "bicycle_count": bicycle_count,
                       "car_count": car_count, "batt": batt})
                print(lora.send_hex(payload))
            except Exception as exc:
                print(f"Measurement error: {exc}", file=sys.stderr)
            elapsed = time.monotonic() - started
            time.sleep(max(0, MEASURE_INTERVAL_SECONDS - elapsed))
    finally:
        gps.close(); sds011.close(); env.close(); line.close()

if __name__ == "__main__":
    main()
