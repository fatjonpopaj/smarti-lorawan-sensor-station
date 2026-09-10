"""GPS reader for NMEA data received through serial."""
import time
import pynmea2
import serial

class GPSFixError(RuntimeError):
    pass

class GPSReader:
    def __init__(self, port, baudrate=9600, timeout=1.0):
        self.serial = serial.Serial(port, baudrate, timeout=timeout)

    def wait_for_fix(self, max_wait_seconds=60.0):
        deadline = time.monotonic() + max_wait_seconds
        while time.monotonic() < deadline:
            raw = self.serial.readline().decode(errors="ignore").strip()
            if not raw.startswith("$"):
                continue
            try:
                msg = pynmea2.parse(raw)
            except pynmea2.ParseError:
                continue
            lat = getattr(msg, "latitude", None)
            lon = getattr(msg, "longitude", None)
            if lat and lon:
                return float(lat), float(lon)
        raise GPSFixError("No valid GPS fix received within the timeout")

    def close(self):
        self.serial.close()
