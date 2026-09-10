"""Binary payload encoding for Smarti LoRaWAN uplinks."""
import struct
import time

LOGIN_TYPE = 0x01
MEASURE_TYPE = 0x02

def _u8(value):
    return max(0, min(255, int(value)))

def _u16_tenths(value):
    return max(0, min(65535, int(round(value * 10))))

def _i16_tenths(value):
    return max(-32768, min(32767, int(round(value * 10))))

def encode_login(station_id, latitude, longitude):
    lon_raw = int(round(longitude * 1_000_000))
    lat_raw = int(round(latitude * 1_000_000))
    return struct.pack(">BQii", LOGIN_TYPE, int(station_id), lon_raw, lat_raw)

def encode_measure(station_id, *, pm25, pm10, temperature, humidity,
                   line_tracker, person_count, bicycle_count, car_count,
                   batt=99, timestamp=None):
    now = int(time.time()) if timestamp is None else int(timestamp)
    return struct.pack(
        ">BQIHHhHBBBBB",
        MEASURE_TYPE,
        int(station_id),
        now,
        _u16_tenths(pm25),
        _u16_tenths(pm10),
        _i16_tenths(temperature),
        _u16_tenths(humidity),
        _u8(line_tracker),
        _u8(person_count),
        _u8(bicycle_count),
        _u8(car_count),
        _u8(batt),
    )
