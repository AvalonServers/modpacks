import os
import sys
import json
import shutil
import appdirs
import argparse
import packlib
import tempfile
import subprocess


def update_instgroups(root: str, name: str):
    """
    Updates the MultiMC instgroups.json file.
    Note that MultiMC needs to be restarted for this file to be re-read.
    """
    groups_data = {
        "formatVersion": "1",
        "groups": {}
    }

    instances_path = f"{root}/instances"
    if os.path.exists(instances_path):
        with open(f"{instances_path}/instgroups.json") as f:
            groups_data = json.load(f)
    
    key = "Packwiz Test Instances"
    if key in groups_data["groups"]:
        instances = groups_data["groups"][key]["instances"]
        instances.append(name)
        groups_data["groups"][key]["instances"] = list(set(instances))
    else:
        groups_data["groups"][key] = {
            "hidden": False,
            "instances": [name]
        }
    
    os.makedirs(instances_path, exist_ok=True)
    with open(f"{instances_path}/instgroups.json", "w") as f:
        json.dump(groups_data, f, indent=4)

def write_error(text: str):
    print(text, file=sys.stderr)

parser = argparse.ArgumentParser(description="Tool for testing packs locally via PolyMC")
parser.add_argument("-p", "--pack", required=True, help="The pack name, i.e. ascent-frozenhell.")

args = parser.parse_args()

pack_path = packlib.get_pack_dir(os.curdir, args.pack)

mmc_pack_name = f"packwiz-test-{args.pack}"
mmc_path = appdirs.user_data_dir("polymc")
if not os.path.exists(mmc_path):
    write_error("PolyMC data folder not found. Do you have PolyMC installed?")
    write_error(f"(the folder that could not be found: {mmc_path})")
    exit(1)

instance_path = f"{mmc_path}/instances/{mmc_pack_name}"

endpoint = f"http://127.0.0.1:8080/pack.toml"
writer = packlib.MMCPackWriter(mmc_pack_name, pack_path, endpoint_override=endpoint)
writer._pack["name"] = writer._pack["name"]

# update the multimc groups
update_instgroups(mmc_path, mmc_pack_name)

# copy the icon
shutil.copyfile("data/test-instance.png", f"{mmc_path}/icons/packwiz-test.png")

# sync the pack files
print("copying pack files...")
with tempfile.TemporaryDirectory() as tmpdir:
    writer.write(tmpdir, {"iconKey": "packwiz-test"})
    os.makedirs(instance_path, exist_ok=True)
    shutil.copytree(tmpdir, instance_path, dirs_exist_ok=True, ignore=shutil.ignore_patterns("instance.cfg", "icon.png"))

    # we don't want to overwrite changes to instance.cfg
    if not os.path.exists(f"{instance_path}/instance.cfg"):
        shutil.copyfile(f"{tmpdir}/instance.cfg", f"{instance_path}/instance.cfg")

# start the server
print("starting packwiz server...")
server = subprocess.Popen(["packwiz", "serve"], cwd=pack_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("starting polymc...")
client = subprocess.Popen(["polymc", "-l", mmc_pack_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

server.wait()
client.wait()
