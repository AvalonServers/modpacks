#!/usr/bin/env bash
set -euo pipefail

curdir="$PWD"

for folder in packs/*/*; do
    pack="$(echo "$folder" | cut -d/ -f2- | tr / -)"

    echo "building mmc zip for $pack"
    mkdir -p "$curdir/build/mmc"
    python3 scripts/export-pack.py -p "$pack"
done
