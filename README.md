# Avalon Minecraft

This repository holds configuration for building Minecraft modpacks that are part of the Descent and Ascent series.

Currently PackWiz is used to build and deploy our packs.

The current packs are:
- Legacy:
    - Uncontainable
    - Nullifaction
- Descent:
    - Infinity
    - Infinity: Expert Mode
    - Cityscape
    - Frozen Hell
- Ascent:
    - Frozen Hell
    - Block One

## Local development

1. Ensure you have MultiMC installed.
2. Install Packwiz with `go install github.com/packwiz/packwiz@latest`.
3. Run `pip install -r requirements.txt` to install the Python requirements.
4. From the root folder, run `python3 ./scripts/test-pack.py -p <pack>`.
5. The pack will automatically be imported into MultiMC and MultiMC will open and start the instance.

## Fixing up packs

A bug in Packwiz currently means that mods that have URLs with special characters will break the launcher. As a workaround, there is a script to rename mods so they are compliant. Run `python3 ./scripts/fixup-pack.py` with the path to the pack as the single argument.

## Deploying

To deploy to the server, merge any related pull requests and then create a GitHub release.
