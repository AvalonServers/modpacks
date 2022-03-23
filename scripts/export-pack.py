import os
import argparse
import packlib
import shutil
import tempfile

parser = argparse.ArgumentParser(description="Tool for creating packs of Packwiz packs")
parser.add_argument("-p", "--pack", required=True, help="The pack name, i.e. ascent-frozenhell.")
parser.add_argument("-d", "--dest-zip", default=f"{os.curdir}/build/mmc", help="The output location of the built zip.")

args = parser.parse_args()

pack_path = packlib.get_pack_dir(os.curdir, args.pack)
writer = packlib.PackWriter(args.pack, pack_path)

with tempfile.TemporaryDirectory() as tmpdir:
    writer.write(tmpdir)
    os.makedirs(args.dest_zip, exist_ok=True)
    shutil.make_archive(f"{args.dest_zip}/{args.pack}", "zip", tmpdir)
