# LoRaWAN Payload Protocol

The station uses compact binary payloads to keep LoRaWAN uplinks small.

All multi-byte values use **big-endian** byte order.

## Message types

| Type | Hex | Length | Purpose |
|---|---:|---:|---|
| Login | `0x01` | 17 bytes | Register station identity and GPS position |
| Measure | `0x02` | 26 bytes | Send current sensor and traffic values |

## Login payload

```text
Offset  Size  Field
0       1     message_type = 0x01
1       8     station_id (uint64)
9       4     longitude * 1,000,000 (int32)
13      4     latitude  * 1,000,000 (int32)
```

Coordinates are multiplied by one million so they can be transferred as integers.

Python representation:

```python
struct.pack(">BQii", 0x01, station_id, lon_raw, lat_raw)
```

## Measure payload

```text
Offset  Size  Field
0       1     message_type = 0x02
1       8     station_id (uint64)
9       4     UNIX timestamp (uint32)
13      2     PM2.5 * 10 (uint16)
15      2     PM10 * 10 (uint16)
17      2     temperature * 10 (int16)
19      2     humidity * 10 (uint16)
21      1     line_tracker (uint8)
22      1     person_count (uint8)
23      1     bicycle_count (uint8)
24      1     car_count (uint8)
25      1     batt (uint8)
```

Python representation:

```python
struct.pack(
    ">BQIHHhHBBBBB",
    0x02,
    station_id,
    timestamp,
    pm25,
    pm10,
    temperature,
    humidity,
    line_tracker,
    person_count,
    bicycle_count,
    car_count,
    batt,
)
```

## Why binary instead of JSON?

A JSON representation is easier to read but considerably larger. The binary protocol minimizes airtime and payload size, which is better suited to LoRaWAN.

The corresponding decoder is located at:

```text
ttn/uplink_payload_formatter.js
```
