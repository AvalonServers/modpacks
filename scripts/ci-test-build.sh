#!/usr/bin/env bash
set -euo pipefail

errored=false
for folder in packs/*/*; do
    hash_before=$(sha256sum "$folder/index.toml")
    (cd "$folder" && packwiz refresh > /dev/null)
    hash_after=$(sha256sum "$folder/index.toml")

    if [[ "$hash_before" != "$hash_after" ]]; then
        echo "error: packwiz refresh caused an update for pack $folder; check the pack is up to date"
        errored=true
    fi
done

if [[ $errored == true ]]; then
    echo "one or more errors occurred validating the configuration"
    exit 1
fi
