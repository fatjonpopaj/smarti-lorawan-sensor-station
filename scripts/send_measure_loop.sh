#!/usr/bin/env bash
set -euo pipefail

INTERVAL="${SMARTI_MEASURE_INTERVAL:-30}"

while true; do
  python src/station.py
  sleep "$INTERVAL"
done
