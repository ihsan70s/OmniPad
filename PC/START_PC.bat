@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" call SETUP_PC.bat
if errorlevel 1 exit /b 1
echo OmniPad LIVE - HP dengan tautan pairing dapat mengontrol PC ini.
echo Gunakan Wi-Fi pribadi. Tekan Ctrl+C untuk berhenti.
".venv\Scripts\python.exe" server.py --live %*
pause
