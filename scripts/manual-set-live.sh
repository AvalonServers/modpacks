#!/usr/bin/env bash
# manually sync and set a pack live on the server outside of CI
pack_name="$1"
pack_subpath=$(echo "$pack_name" | tr - /)
pack_path="packs/$pack_subpath"

echo "Uploading pack to CDN"
python3 scripts/export-pack.py -p "$pack_name"

aws s3 cp \
    --endpoint-url=https://s3.eu-west-1.wasabisys.com \
    --profile=wasabi_arctarus_avalon \
    --acl public-read \
    "build/mmc/$pack_name.zip" "s3://avalon-assets/packs/mmc/$pack_name.zip"
aws s3 sync \
    --endpoint-url=https://s3.eu-west-1.wasabisys.com \
    --profile=wasabi_arctarus_avalon \
    --delete --acl public-read \
    "$pack_path" "s3://avalon-assets/data/$pack_subpath"

# echo "Reconfiguring the Minecraft server"

read -r -d '' supervisor_config_file <<EOF
[program:avalon-$pack_name]
command=/var/lib/avalon/mc/$pack_subpath/start.sh
directory=/var/lib/avalon/mc/$pack_subpath
user=avalon
group=avalon
autostart=true
autorestart=true
stopasgroup=true
stopsignal=QUIT
EOF

forge_version="1.12.2-14.23.5.2860"
forge_url="https://maven.minecraftforge.net/net/minecraftforge/forge/$forge_version/forge-$forge_version-installer.jar"

ssh psn-worker-1.home.alex0.net <<EOF
echo "$supervisor_config_file" | sudo tee /etc/supervisor/conf.d/avalon-$pack_name.conf >/dev/null

echo "Stopping the Minecraft server"
sudo supervisorctl stop "avalon-$pack_name"

echo "Installing the server"
sudo -i -u avalon bash -c 'cd /var/lib/avalon/mc/$pack_subpath && wget "$forge_url" -O forge-installer.jar && java -jar ./forge-installer.jar --installServer'
sudo -i -u avalon bash -c 'cd /var/lib/avalon/mc/$pack_subpath && ln -sf "forge-$forge_version.jar" "server.jar"'

echo "Installing the modpack"
sudo mkdir -p "/var/lib/avalon/mc/$pack_subpath"
sudo chmod -R 0770 /var/lib/avalon/mc/$pack_subpath
sudo chown -R avalon:avalon /var/lib/avalon/mc/$pack_subpath
sudo -i -u avalon bash -c 'cd /var/lib/avalon/mc/$pack_subpath && java -Xmx4G -jar /var/lib/avalon/mc/packwiz-installer-bootstrap.jar -g -s server https://s3.eu-west-1.wasabisys.com/avalon-assets/data/$pack_subpath/pack.toml'
sudo -i -u avalon bash -c 'cd /var/lib/avalon/mc/$pack_subpath && chmod +x ./start.sh'

echo "Starting the server"
sudo supervisorctl reload
sudo supervisorctl start "avalon-$pack_name"

echo "Operation completed"
EOF