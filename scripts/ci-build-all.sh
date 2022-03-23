#!/usr/bin/env bash
set -euo pipefail

curdir="$PWD"

for folder in packs/*/*; do
    pack="$(echo "$folder" | cut -d/ -f2- | tr / -)"

    echo "building mmc zip for $pack"
    mkdir -p "$curdir/build/mmc"
    python3 scripts/export-pack.py -p "$pack"

    echo "building modrinth pack for $pack"
    mkdir -p "$curdir/build/modrinth"
    (cd "$folder" && packwiz modrinth "export" -o "$curdir/build/modrinth/$pack.mrpack")
done
