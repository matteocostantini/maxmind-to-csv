# maxmind-to-csv

```powershell
cp config.yaml.example config.yaml
```

```powershell
Get-ChildItem -Directory -Filter "geoipupdate_*" | Remove-Item -Recurse -Force
.\geoipupdate-latest-release.ps1
```

```powershell
Remove-Item .geoipupdate.lock
.\<geoipupdate_folder>\geoipupdate.exe -f .\GeoIP.conf -d .
```