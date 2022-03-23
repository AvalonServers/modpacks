from logging import root
import os
import sys
import toml
import json
import tempfile
import argparse
import urllib.request
import shutil
import configparser

DOWNLOAD_ENDPOINT = "https://avalonservers.github.io/modpacks/packs"
INSTALLER_BOOTSTRAPPER_ENDPOINT = "https://github.com/packwiz/packwiz-installer-bootstrap/releases/latest/download/packwiz-installer-bootstrap.jar"

parser = argparse.ArgumentParser(description="Tool for creating packs of Packwiz packs")
parser.add_argument("-p", "--pack", required=True, help="The pack name, i.e. ascent-frozenhell.")
parser.add_argument("-d", "--dest-zip", default=f"{os.curdir}/build/mmc", help="The output location of the built zip.")

class PackWriter():
    def __init__(self, slug, pack_root: str):
        if not os.path.isdir(pack_root):
            raise Exception("The specified pack does not exist")

        self._slug = slug
        self._pack_root = pack_root

        # read the pack metadata
        with open(f"{pack_root}/pack.toml") as f:
            self._pack = toml.load(f)
    
    def _write_mmc_pack_json(self, output: str):
        components = [{
            "important": True,
            "uid": "net.minecraft",
            "version": self._pack["versions"]["minecraft"]
        }]

        # add the modloader
        if "forge" in self._pack["versions"]:
            components.append({
                "uid": "net.minecraftforge",
                "version": self._pack["versions"]["forge"]
            })
        elif "fabric" in self._pack["versions"]:
            components.append({
                "uid": "net.fabricmc.fabric-loader",
                "version": self._pack["versions"]["fabric"]
            })

        result = {
            "components": components,
            "formatVersion": 1
        }

        with open(output, "w") as f:
            json.dump(result, f, indent=4)

    def _write_instance_cfg_ini(self, output: str):
        # build the URL used to download the pack
        pack_meta_url = DOWNLOAD_ENDPOINT
        for pack_comp in self._slug.split("-"):
            pack_meta_url = f"{pack_meta_url}/{pack_comp}"
        pack_meta_url = f"{pack_meta_url}/pack.toml"

        attributes = {
            "InstanceType": "OneSix",
            "OverrideCommands": True,
            "PreLaunchCommand": f"\"$INST_JAVA\" -jar packwiz-installer-bootstrap.jar {pack_meta_url}",
            "name": self._pack["name"],
        }

        if os.path.exists(f"{self._pack_root}/icon.png"):
            attributes["iconKey"] = "icon"

        config = ""
        for k, v in attributes.items():
            if isinstance(v, bool):
                v = str.lower(str(v))
            config = config + f"{k}={v}\n"
        config = config.strip()

        with open(output, "w") as f:
            f.write(config)

    def write(self, output: str):
        # create temporary dir
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_mmc_pack_json(f"{tmpdir}/mmc-pack.json")
            self._write_instance_cfg_ini(f"{tmpdir}/instance.cfg")

            # copy the icon
            icon_path = f"{self._pack_root}/icon.png"
            if os.path.exists(icon_path):
                shutil.copyfile(icon_path, f"{tmpdir}/icon.png")

            # create minecraft dir
            os.mkdir(f"{tmpdir}/.minecraft")

            # download the launcher boot strapper
            urllib.request.urlretrieve(INSTALLER_BOOTSTRAPPER_ENDPOINT, f"{tmpdir}/.minecraft/packwiz-installer-bootstrap.jar")

            # create the archive
            os.makedirs(output, exist_ok=True)
            shutil.make_archive(f"{output}/{self._slug}", "zip", tmpdir)

args = parser.parse_args()

root_dir = os.curdir
pack_path = f"{root_dir}/packs"
for pack_comp in args.pack.split("-"):
    pack_path = f"{pack_path}/{pack_comp}"

writer = PackWriter(args.pack, pack_path)
writer.write(args.dest_zip)
