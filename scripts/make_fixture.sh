#!/usr/bin/env bash
# Regenerate fixtures/hello.wav (synthetic speech for smoke tests).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/fixtures"
RAW="/tmp/vtl_hello_raw.wav"
OUT="$ROOT/fixtures/hello.wav"

if command -v espeak-ng >/dev/null 2>&1; then
  espeak-ng -v en-us -s 140 -w "$RAW" "Hello, this is a voice turn taking lab test."
elif command -v say >/dev/null 2>&1; then
  say -o /tmp/vtl_hello_raw.aiff "Hello, this is a voice turn taking lab test."
  if command -v ffmpeg >/dev/null 2>&1; then
    ffmpeg -y -i /tmp/vtl_hello_raw.aiff -ar 16000 -ac 1 "$OUT"
    echo "wrote $OUT (via say + ffmpeg)"
    exit 0
  else
    echo "stop_reason: say worked but ffmpeg missing — brew install ffmpeg"
    exit 1
  fi
else
  echo "stop_reason: need espeak-ng or macOS say to build fixture"
  exit 1
fi

if command -v ffmpeg >/dev/null 2>&1; then
  ffmpeg -y -i "$RAW" -ar 16000 -ac 1 "$OUT"
else
  cp "$RAW" "$OUT"
fi
echo "wrote $OUT"
