# Architecture

## Sensor-station role

The Smarti sensor station is the edge component responsible for acquiring real-world data and transmitting compact measurements into the Smarti platform.

```mermaid
flowchart TD
    A[BME280] --> P[Raspberry Pi 4]
    B[SDS011] --> P
    C[Line Tracker / GPIO17] --> P
    D[GPS / NMEA] --> P
    E[Camera + MediaPipe] --> P
    P --> F[Binary Payload Encoder]
    F --> G[LoRa-E5 via UART / AT commands]
    G --> H[LoRaWAN]
    H --> I[The Things Network]
    I --> J[TTN Uplink Formatter]
    J --> K[Backend]
    K --> L[Frontend / Monitoring]
```

## Responsibilities

The Raspberry Pi acts as the local controller. It:

- reads environmental and particulate-matter sensors,
- obtains the current GPS position,
- reads the digital line-tracker state,
- consumes locally produced traffic counts,
- stores a persistent station identity,
- encodes login and measurement messages,
- controls the LoRaWAN module through serial AT commands,
- transmits uplinks to The Things Network.

The design intentionally sends compact values rather than images. Camera frames are processed locally and only the resulting counters are forwarded.

## Interfaces

| Component | Interface | Purpose |
|---|---|---|
| BME280 | I²C | Temperature and humidity |
| SDS011 | UART / serial | PM2.5 and PM10 |
| GPS module | UART / serial | NMEA position data |
| Line tracker | GPIO17 | Digital status |
| Camera Module 3 Wide | CSI / libcamera | Local object detection |
| LoRa-E5 | UART / serial | LoRaWAN AT-command communication |
