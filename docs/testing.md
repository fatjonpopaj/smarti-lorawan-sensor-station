# Testing

The project combines hardware-dependent tests on the Raspberry Pi with platform-independent protocol tests.

## Automated protocol tests

Run:

```bash
python -m unittest discover -s tests -v
```

The tests verify:

- login payload length,
- measure payload length,
- byte order,
- signed temperature handling,
- field positions,
- coordinate scaling.

## BME280

Check whether the sensor is visible:

```bash
i2cdetect -y 1
```

The prototype used address:

```text
0x76
```

## LoRa-E5

Test the serial module:

```bash
python scripts/test_lora_at.py
```

Typical AT commands are:

```text
AT+ID
AT+NJS
AT+JOIN
```

A successful uplink typically ends with:

```text
+MSGHEX: Done
```

## Camera

Check OpenCV:

```bash
python -c "import cv2; print('cv2 ok')"
```

The Raspberry Pi Camera Module 3 Wide was detected as an `imx708_wide` device during development.

The camera process writes the latest counters to a JSON file. The station rejects the file if it is older than 10 seconds.

## Runtime counter file

Example:

```bash
cat runtime/latest_counts.json
```

Expected shape:

```json
{
  "type": "measure",
  "id": 101,
  "time": 0,
  "readings": {
    "person_count": 0,
    "bicycle_count": 0,
    "car_count": 0
  }
}
```
