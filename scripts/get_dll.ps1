$ErrorActionPreference = "Stop"
$url = "https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases/download/v0.9.6/LibreHardwareMonitor.zip"
$dest = "app/services/metrics/lib"
$zip = "$env:TEMP\lhm-release.zip"
$tmp = "$env:TEMP\lhm-release"

Invoke-WebRequest $url -OutFile $zip
Expand-Archive $zip -DestinationPath $tmp -Force
New-Item -ItemType Directory -Force $dest | Out-Null
Copy-Item "$tmp\*.dll" $dest -Force

try { Remove-Item $tmp -Recurse -Force -ErrorAction Stop } catch {}
try { Remove-Item $zip -Force -ErrorAction Stop } catch {}

Write-Host "DLLs instalados en $dest"
