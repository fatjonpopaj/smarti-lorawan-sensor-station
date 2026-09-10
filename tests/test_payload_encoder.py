import struct
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lorawan.payload_encoder import encode_login, encode_measure


class PayloadEncoderTests(unittest.TestCase):
    def test_login_length_and_type(self):
        payload = encode_login(101, latitude=52.0, longitude=9.0)
        self.assertEqual(len(payload), 17)
        self.assertEqual(payload[0], 0x01)

    def test_login_fields(self):
        payload = encode_login(101, latitude=52.123456, longitude=9.654321)
        msg_type, station_id, lon_raw, lat_raw = struct.unpack(">BQii", payload)
        self.assertEqual(msg_type, 0x01)
        self.assertEqual(station_id, 101)
        self.assertEqual(lon_raw, 9_654_321)
        self.assertEqual(lat_raw, 52_123_456)

    def test_measure_length_and_type(self):
        payload = encode_measure(
            101,
            timestamp=1_700_000_000,
            pm25=12.3,
            pm10=45.6,
            temperature=21.7,
            humidity=48.2,
            line_tracker=1,
            person_count=2,
            bicycle_count=3,
            car_count=4,
            batt=99,
        )
        self.assertEqual(len(payload), 26)
        self.assertEqual(payload[0], 0x02)

    def test_measure_roundtrip(self):
        payload = encode_measure(
            101,
            timestamp=1_700_000_000,
            pm25=12.3,
            pm10=45.6,
            temperature=-3.4,
            humidity=48.2,
            line_tracker=1,
            person_count=2,
            bicycle_count=3,
            car_count=4,
            batt=99,
        )

        values = struct.unpack(">BQIHHhHBBBBB", payload)

        self.assertEqual(values[0], 0x02)
        self.assertEqual(values[1], 101)
        self.assertEqual(values[2], 1_700_000_000)
        self.assertEqual(values[3], 123)
        self.assertEqual(values[4], 456)
        self.assertEqual(values[5], -34)
        self.assertEqual(values[6], 482)
        self.assertEqual(values[7:], (1, 2, 3, 4, 99))


if __name__ == "__main__":
    unittest.main()
