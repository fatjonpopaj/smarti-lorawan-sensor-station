"""Simple serial diagnostic for a LoRa-E5 compatible AT-command module."""

from __future__ import annotations

import os
import time

import serial


def main() -> None:
    port = os.getenv("LORA_PORT")
    if not port:
        raise SystemExit("Set LORA_PORT before running this script.")

    baud = int(os.getenv("LORA_BAUD", "9600"))

    with serial.Serial(port, baud, timeout=2) as ser:
        for command in ("AT+ID", "AT+NJS"):
            ser.reset_input_buffer()
            ser.write((command + "\r\n").encode("ascii"))
            ser.flush()
            time.sleep(2)
            response = ser.read_all().decode(errors="replace").strip()
            print(f">>> {command}")
            print(response or "<no response>")


if __name__ == "__main__":
    main()
