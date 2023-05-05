#!/usr/bin/env bash
rm -rf dist
pyinstaller --clean -y -F  -n MaxMindDB-to-CSV -i logo.ico main.py
cp config.yaml dist/config.yaml
cp IP.csv dist/.
cp tools/geoip_convert-v2-v1.sh dist/geoip_convert-v2-v1.sh
#/usr/share/GeoIP/GeoIP.dat
bash dist/MaxMindDB-to-CSV --update
