#!/usr/bin/env bash
set -euo pipefail

# currently, this script is only applicable to reika's packs
(cd packs/special/dragon-realm && python3 ./tools/update-reika-mods.py)
