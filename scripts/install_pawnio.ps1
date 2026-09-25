$ErrorActionPreference = "Stop"
$reg = Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\PawnIO" -ErrorAction SilentlyContinue
if ($reg) {
    Write-Host "PawnIO ya esta instalado ($($reg.DisplayVersion))"
    exit 0
}

$url = "https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/raw/refs/heads/master/LibreHardwareMonitor.Windows.Forms/Resources/PawnIO_setup.exe"
$installer = "$env:TEMP\PawnIO_setup.exe"

Invoke-WebRequest -Uri $url -OutFile $installer
Start-Process -FilePath $installer -ArgumentList "-install","-silent" -Verb RunAs -Wait
Remove-Item $installer -Force -ErrorAction SilentlyContinue

Start-Sleep -Seconds 2
$reg = Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\PawnIO" -ErrorAction SilentlyContinue
if ($reg) {
    Write-Host "PawnIO instalado ($($reg.DisplayVersion))"
} else {
    Write-Host "PawnIO NO se pudo instalar"
    exit 1
}
