# Troubleshooting

## BME280 is not detected

Symptoms:

- no measurement,
- I²C errors,
- device missing from the expected address.

Check:

```bash
i2cdetect -y 1
```

The prototype used `0x76`.

## No valid SDS011 frame

The reader expects:

```text
AA C0 ... checksum AB
```

Check:

- correct serial port,
- 9600 baud,
- USB/UART adapter availability,
- sensor power supply.

## GPS has no position

A GPS receiver can need time to obtain a satellite fix.

The software ignores invalid or incomplete NMEA data and waits for a valid latitude/longitude pair.

Check:

- serial port,
- baud rate,
- outdoor / near-window reception,
- incoming NMEA sentences.

## LoRaWAN uplink is not visible

Check the communication chain in this order:

1. `AT+ID`
2. `AT+NJS`
3. `AT+JOIN`
4. `AT+MSGHEX="..."`

If the LoRa module reports success but the decoded data is wrong, inspect the TTN uplink formatter and payload offsets.

## Camera data is stale

The station intentionally raises an error when the counter file is missing or older than 10 seconds.

Start the camera process first and verify that the JSON timestamp/file modification time is updating.

## Old cumulative camera counts

During development, stale cumulative counts were observed after restarting the camera process.

For a clean run:

- start counters from zero,
- avoid loading stale runtime state,
- remove old `latest_counts.json` before testing when necessary.
