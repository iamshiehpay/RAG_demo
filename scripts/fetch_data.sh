#!/usr/bin/env bash
# Download the test documents into data/. Pinned versions keep tests reproducible.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data

fetch() {
  local url="$1" out="$2" checksum="${3:-}"
  if [[ -f "$out" ]]; then
    echo "exists: $out"
  else
    curl -fsSL --retry 2 -o "$out" "$url"
    echo "downloaded: $out"
  fi
  if [[ -n "$checksum" ]]; then
    python3 - "$out" "$checksum" <<'PY'
import hashlib
import sys
from pathlib import Path

actual = hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest()
if actual != sys.argv[2]:
    raise SystemExit(f"SHA256 mismatch for {sys.argv[1]}: {actual}")
print(f"verified: {sys.argv[1]} ({actual})")
PY
  fi
}

fetch https://arxiv.org/pdf/2410.05779v3 data/lightrag.pdf
fetch https://arxiv.org/pdf/2603.06749v1 data/industrial-robotics.pdf \
  8ab9a63ca99b0b26432e7a4d6b4c2810d00b97a2df1791973fe2d7d321ede0b9
