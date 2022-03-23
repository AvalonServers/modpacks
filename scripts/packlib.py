import os
import toml
import json
import urllib.request
import shutil

DOWNLOAD_ENDPOINT = "https://cdn.avalon.arctarus.co.uk/data"
INSTALLER_BOOTSTRAPPER_ENDPOINT = "https://github.com/packwiz/packwiz-installer-bootstrap/releases/latest/download/packwiz-installer-bootstrap.jar"

def get_pack_dir(root: str, pack: str):
    path = f"{root}/packs"
    for comp in pack.split("-"):
        path = f"{path}/{comp}"
    return path

class PackWriter():
    def __init__(
        self,
        slug,
        pack_root: str,
        endpoint_override: str = None,
    ):
        if not os.path.isdir(pack_root):
            raise Exception("The specified pack does not exist")

        self._slug = slug
        self._pack_root = pack_root

        if endpoint_override is not None:
            self._pack_meta_url = endpoint_override
        else:
            self._pack_meta_url = DOWNLOAD_ENDPOINT
            for pack_comp in self._slug.split("-"):
                self._pack_meta_url = f"{self._pack_meta_url}/{pack_comp}"
            self._pack_meta_url = f"{self._pack_meta_url}/pack.toml"

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

    def _write_instance_cfg_ini(self, output: str, config: dict):
        attributes = {
            "InstanceType": "OneSix",
            "OverrideCommands": True,
            "PreLaunchCommand": f"\"$INST_JAVA\" -jar packwiz-installer-bootstrap.jar {self._pack_meta_url}",
            "name": self._pack["name"],
        }
        
        if os.path.exists(f"{self._pack_root}/icon.png"):
            attributes["iconKey"] = self._slug
        
        attributes = {**attributes, **config}

        config = ""
        for k, v in attributes.items():
            if isinstance(v, bool):
                v = str.lower(str(v))
            config = config + f"{k}={v}\n"
        config = config.strip()

        with open(output, "w") as f:
            f.write(config)

    def write(self, output: str, config: dict = {}):
        """
        Writes the pack to the specified output directory
        """

        self._write_mmc_pack_json(f"{output}/mmc-pack.json")
        self._write_instance_cfg_ini(f"{output}/instance.cfg", config)

        # copy the icon
        icon_path = f"{self._pack_root}/icon.png"
        if os.path.exists(icon_path):
            shutil.copyfile(icon_path, f"{output}/{self._slug}.png")

        # create minecraft dir
        os.mkdir(f"{output}/.minecraft")

        # download the launcher boot strapper
        urllib.request.urlretrieve(INSTALLER_BOOTSTRAPPER_ENDPOINT, f"{output}/.minecraft/packwiz-installer-bootstrap.jar")
