#!/usr/bin/env bash
# Download the test documents into data/. Pinned versions keep tests reproducible.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data

fetch() {
  local url="$1" out="$2"
  if [[ -f "$out" ]]; then
    echo "exists: $out"
  else
    curl -fsSL -o "$out" "$url"
    echo "downloaded: $out"
  fi
}

fetch https://arxiv.org/pdf/2410.05779v3 data/lightrag.pdf
