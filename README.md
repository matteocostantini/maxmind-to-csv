# geoip2-to-csv

```powershell
cp config.yaml.example config.yaml
```

## Aggiornamento database con `geoipupdate`

1. Download di geoip
   - per Windows

```powershell
Get-ChildItem -Directory -Filter "geoipupdate_*" | Remove-Item -Recurse -Force
.\tools\geoipupdate-latest-release.ps1
```

```powershell
Remove-Item .geoipupdate.lock
.\<geoipupdate_folder>\geoipupdate.exe -f .\GeoIP.conf -d . --parallelism 3
```
   - per Linux ...