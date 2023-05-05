#!/usr/bin/env bash
if [ ! -d "env" ]; then
    echo "Creazione dell'ambiente virtuale Python 2..."
    virtualenv env
fi

if [ ! -d "venv" ]; then
    echo "Creazione dell'ambiente virtuale Python 3..."
    python3 -m venv venv --copies
fi

source ./venv/bin/activate
pip3.9 install -r requirements.txt
rm -rf dist
pyinstaller --clean -y -F  -n MaxMindDB-to-CSV -i logo.ico main.py
deactivate
cp config.yaml.example dist/config.yaml
cd dist/
if [ ! -f IP.csv ]; then
    echo "Creazione del file dalla directory parent!"
    echo "IP\n8.8.8.8" > IP.csv
fi
chmod +x MaxMindDB-to-CSV
./MaxMindDB-to-CSV --update
cp ../tools/geoip_convert-v2-v1.sh ./geoip_convert-v2-v1.sh

if [ -f /usr/share/GeoIP/GeoIP.dat ]; then
    cp GeoIP.dat /usr/share/GeoIP/GeoIP.dat
fi
cd ..
#pip2 install ipaddr
#pip2 install pygeoip