@echo off
setlocal
cd /d "%~dp0"

echo ==^> Cai PyInstaller (neu chua co)...
pip install --upgrade pyinstaller
if errorlevel 1 goto :fail

echo ==^> Don build cu...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist BatteryTray.spec del /q BatteryTray.spec

echo ==^> Build BatteryTray.exe...
python -m PyInstaller ^
    --noconsole ^
    --onefile ^
    --name BatteryTray ^
    --hidden-import PIL._tkinter_finder ^
    --collect-submodules pystray ^
    --collect-submodules PIL ^
    battery_tray.py
if errorlevel 1 goto :fail

if not exist "dist\BatteryTray.exe" goto :fail

echo.
echo ==^> Thanh cong: dist\BatteryTray.exe
dir "dist\BatteryTray.exe" | findstr BatteryTray.exe
echo.
pause
exit /b 0

:fail
echo.
echo ==^> Build that bai
pause
exit /b 1
