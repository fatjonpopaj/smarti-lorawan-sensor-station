# Smarti LoRaWAN Sensor Station

## Overview

This repository contains a cleaned portfolio version of the Raspberry Pi based sensor-station component developed for the **Smarti / LoRaWAN Smart Infrastructure Monitoring** bachelor practice project at Hochschule Hannover.

The station collects environmental, location and traffic-related data, combines the measurements on a Raspberry Pi, encodes them into compact binary payloads and transmits them through a LoRa module to **The Things Network (TTN)**. A TTN uplink formatter converts the binary payload back into structured data for the backend.

Device-specific identifiers, credentials and private infrastructure values are intentionally excluded.

## Architecture

```text
Sensors / GPS / Camera
        |
        v
   Raspberry Pi
        |
        | Python
        v
 Binary Payload Encoder
        |
        v
 LoRa-E5 via UART / AT commands
        |
        v
      LoRaWAN
        |
        v
The Things Network (TTN)
        |
        | JavaScript Uplink Formatter
        v
      Backend
        |
        v
      Frontend
```

## Hardware

- Raspberry Pi 4
- LoRa-E5 compatible LoRaWAN module
- BME280 environmental sensor
- SDS011 particulate matter sensor
- GPS module with NMEA output
- Digital line tracker on GPIO17
- Raspberry Pi Camera Module 3 Wide

## Metrics

`temperature`, `humidity`, `pm25`, `pm10`, `line_tracker`, `person_count`, `bicycle_count`, `car_count`, `batt`

The battery value is simulated in the prototype because no dedicated battery measurement circuit was integrated.

## Technologies

Python, Raspberry Pi OS/Linux, LoRaWAN, The Things Network, UART, I²C, GPIO, NMEA/GPS, MediaPipe, OpenCV, Picamera2/libcamera and JavaScript.

## LoRaWAN Payload Protocol

### Login — 17 bytes

```text
Byte 0      type = 0x01
Byte 1-8    station_id (uint64, big endian)
Byte 9-12   longitude * 1,000,000 (int32)
Byte 13-16  latitude  * 1,000,000 (int32)
```

### Measure — 26 bytes

```text
Byte 0      type = 0x02
Byte 1-8    station_id (uint64)
Byte 9-12   UNIX timestamp (uint32)
Byte 13-14  PM2.5 * 10 (uint16)
Byte 15-16  PM10 * 10 (uint16)
Byte 17-18  temperature * 10 (int16)
Byte 19-20  humidity * 10 (uint16)
Byte 21     line_tracker (uint8)
Byte 22     person_count (uint8)
Byte 23     bicycle_count (uint8)
Byte 24     car_count (uint8)
Byte 25     batt (uint8)
```

## Setup

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip i2c-tools
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp config/station_config.example.json config/station_config.json
```

Enable I²C, serial/UART and the camera interfaces as required by the Raspberry Pi OS version.

The prototype used BME280 address `0x76`. Check I²C devices with:

```bash
i2cdetect -y 1
```

Configure hardware-specific ports through environment variables:

```bash
export LORA_PORT="/dev/serial/by-id/<YOUR_LORA_DEVICE>"
export GPS_PORT="/dev/ttyUSB0"
export SDS011_PORT="/dev/ttyUSB1"
export CAMERA_COUNTS_PATH="/home/pi/ap9_mediapipe/latest_counts.json"
```

Run the station with:

```bash
python src/station.py
```

## Camera-Based Traffic Detection

The camera process runs separately and writes `person_count`, `bicycle_count` and `car_count` to a JSON file consumed by the sensor station. The station rejects camera data older than 10 seconds.

The camera implementation uses MediaPipe Object Detection and is intended for a Raspberry Pi Camera Module 3 Wide. Install Picamera2/libcamera through Raspberry Pi OS and the additional Python packages from `requirements-camera.txt`.

Example:

```bash
python src/camera/traffic_counter.py \
  --model models/efficientdet_lite0.tflite \
  --output runtime/latest_counts.json
```

## TTN Uplink Formatter

Use `ttn/uplink_payload_formatter.js` as the JavaScript uplink formatter in The Things Network. It decodes `0x01` login and `0x02` measure messages.

## University Project Background

Smarti was developed as a bachelor practice project in Applied Computer Science. The overall system combined distributed sensor stations, LoRaWAN communication, backend services, data persistence and a web frontend for monitoring and visualization.

This repository focuses on the **sensor-station side**: hardware integration, Python-based data acquisition, GPS-based station registration, compact binary payload encoding, LoRaWAN communication and camera-based traffic measurements.
