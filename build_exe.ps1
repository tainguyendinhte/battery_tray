# Build BatteryTray.exe standalone bằng PyInstaller
# Yêu cầu: đã cài Python + pip install -r requirements.txt

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "==> Cài PyInstaller (nếu chưa có)..." -ForegroundColor Cyan
pip install --upgrade pyinstaller

Write-Host "==> Dọn build cũ..." -ForegroundColor Cyan
Remove-Item -Recurse -Force build, dist, BatteryTray.spec -ErrorAction SilentlyContinue

Write-Host "==> Build BatteryTray.exe..." -ForegroundColor Cyan
pyinstaller `
    --noconsole `
    --onefile `
    --name BatteryTray `
    --hidden-import PIL._tkinter_finder `
    --collect-submodules pystray `
    --collect-submodules PIL `
    battery_tray.py

if (Test-Path "dist\BatteryTray.exe") {
    $size = (Get-Item "dist\BatteryTray.exe").Length / 1MB
    Write-Host ("==> Thanh cong: dist\BatteryTray.exe ({0:N1} MB)" -f $size) -ForegroundColor Green
} else {
    Write-Host "==> Build that bai" -ForegroundColor Red
    exit 1
}
