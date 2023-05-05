#!/usr/bin/env bash
rm -rf dist
pyinstaller --clean -y -F  -n MaxMindDB-to-CSV -i logo.ico main.py
cp config.yaml.example dist/config.yaml
cp IP.csv dist/.
