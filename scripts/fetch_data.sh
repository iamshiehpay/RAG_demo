#!/usr/bin/env bash
# Download fixed public versions atomically; PDFs remain gitignored.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data

verify() {
  python3 - "$1" "$2" <<'PY'
import hashlib
import sys
from pathlib import Path

actual = hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest()
if actual != sys.argv[2]:
    raise SystemExit(f"SHA256 mismatch for {sys.argv[1]}: {actual}")
PY
}

fetch() {
  local url="$1" out="$2" checksum="$3" temporary
  if [[ -f "$out" ]]; then
    verify "$out" "$checksum"
    echo "verified existing: $out"
    return
  fi
  temporary="$(mktemp "$out.XXXXXX")"
  if ! curl -fsSL --retry 2 -o "$temporary" "$url" || ! verify "$temporary" "$checksum"; then
    rm -f "$temporary"
    return 1
  fi
  mv "$temporary" "$out"
  echo "downloaded and verified: $out"
}

fetch https://arxiv.org/pdf/2410.05779v3 data/lightrag.pdf \
  bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a
fetch https://arxiv.org/pdf/2603.06749v1 data/industrial-robotics.pdf \
  8ab9a63ca99b0b26432e7a4d6b4c2810d00b97a2df1791973fe2d7d321ede0b9
