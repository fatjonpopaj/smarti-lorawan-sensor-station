# Hardware

## Core components

| Component | Role |
|---|---|
| Raspberry Pi 4 | Central controller and edge-processing device |
| LoRa-E5 compatible module | LoRaWAN communication |
| BME280 | Temperature and humidity measurement |
| SDS011 | PM2.5 and PM10 particulate-matter measurement |
| GPS module | Station positioning through NMEA data |
| Line Tracker | Additional digital sensor |
| Raspberry Pi Camera Module 3 Wide | Traffic-object detection |

## Known connections

### BME280

- Interface: I²C
- Bus: `1`
- Prototype address: `0x76`

Check the device with:

```bash
i2cdetect -y 1
```

### Line Tracker

- Signal: GPIO17
- Physical Raspberry Pi pin: 11
- Output: digital `0` or `1`

### SDS011

The SDS011 produces a 10-byte measurement frame.

Relevant frame properties:

```text
Header: AA C0
PM2.5: bytes 2-3
PM10:  bytes 4-5
Checksum: byte 8
End: AB
```

The values are encoded in tenths of µg/m³.

## Hardware-specific configuration

Serial device names can vary between Raspberry Pi installations. They are therefore not hard-coded in this repository.

Use environment variables instead:

```bash
export LORA_PORT="/dev/serial/by-id/<YOUR_LORA_DEVICE>"
export GPS_PORT="/dev/ttyUSB0"
export SDS011_PORT="/dev/ttyUSB1"
```
