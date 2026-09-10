"""Minimal SDS011 PM2.5/PM10 frame reader."""
import time
import serial

class SDS011Error(RuntimeError):
    pass

class SDS011Reader:
    def __init__(self, port, baudrate=9600, timeout=2.0):
        self.serial = serial.Serial(port, baudrate, timeout=timeout)

    @staticmethod
    def _decode(frame):
        if len(frame) != 10 or frame[0] != 0xAA or frame[1] != 0xC0 or frame[9] != 0xAB:
            raise SDS011Error("Invalid SDS011 frame")
        if sum(frame[2:8]) % 256 != frame[8]:
            raise SDS011Error("Invalid SDS011 checksum")
        pm25 = (frame[2] + frame[3] * 256) / 10.0
        pm10 = (frame[4] + frame[5] * 256) / 10.0
        return pm25, pm10

    def read(self, max_wait_seconds=8.0):
        deadline = time.monotonic() + max_wait_seconds
        while time.monotonic() < deadline:
            if self.serial.read(1) != b"\xAA":
                continue
            if self.serial.read(1) != b"\xC0":
                continue
            rest = self.serial.read(8)
            if len(rest) != 8:
                continue
            try:
                return self._decode(b"\xAA\xC0" + rest)
            except SDS011Error:
                continue
        raise SDS011Error("No valid SDS011 frame received")

    def close(self):
        self.serial.close()
