#!/usr/bin/env bash
# Regenerate fixtures/hello.wav (synthetic espeak speech for smoke tests).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/fixtures"
espeak-ng -v en-us -s 140 -w /tmp/vtl_hello_raw.wav "Hello, this is a voice turn taking lab test."
ffmpeg -y -i /tmp/vtl_hello_raw.wav -ar 16000 -ac 1 "$ROOT/fixtures/hello.wav"
echo "wrote $ROOT/fixtures/hello.wav"
