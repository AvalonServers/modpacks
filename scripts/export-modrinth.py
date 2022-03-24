import os
import argparse
import packlib

parser = argparse.ArgumentParser(description="Tool for uploading packs to Modrinth")
parser.add_argument("-p", "--pack", required=True, help="The pack name, i.e. ascent-frozenhell.")
parser.add_argument("-t", "--token", default=os.environ.get("AVALON_MODRINTH_TOKEN"), help="The token to use to authenticate to Modrinth")

args = parser.parse_args()
pack_path = packlib.get_pack_dir(os.curdir, args.pack)

uploader = packlib.ModrinthPackUploader(args.pack, pack_path, args.token)
uploader.upload()
