#!/usr/bin/env bash
set -euo pipefail

OUTPUT_DIR="${1:-artifacts/hardware}"
mkdir -p "$OUTPUT_DIR"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUTPUT="$OUTPUT_DIR/jetson-inventory-$STAMP.txt"

{
  echo "SYNQAGI Jetson read-only inventory"
  echo "timestamp_utc=$STAMP"
  echo
  echo "== uname =="
  uname -a || true
  echo
  echo "== os-release =="
  cat /etc/os-release 2>/dev/null || true
  echo
  echo "== nv_tegra_release =="
  cat /etc/nv_tegra_release 2>/dev/null || true
  echo
  echo "== model =="
  cat /proc/device-tree/model 2>/dev/null || true
  echo
  echo "== memory =="
  free -h || true
  echo
  echo "== storage =="
  df -h || true
  echo
  echo "== nvcc =="
  nvcc --version 2>/dev/null || true
  echo
  echo "== tensorrt packages =="
  dpkg -l 2>/dev/null | grep -i tensorrt || true
  echo
  echo "== nvpmodel =="
  nvpmodel -q 2>/dev/null || true
  echo
  echo "== tegrastats availability =="
  command -v tegrastats || true
} | tee "$OUTPUT"

echo "Inventory written to $OUTPUT"
