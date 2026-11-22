@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" call SETUP_PC.bat
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -c "import aiortc,mss,PIL" >nul 2>&1
if errorlevel 1 call SETUP_PC.bat
if errorlevel 1 exit /b 1
echo OmniPad LIVE + SCREEN - HP pemilik tautan dapat melihat layar PC jika Mulai layar ditekan.
echo Gunakan Wi-Fi pribadi. Tekan Ctrl+C untuk menghentikan akses dan siaran.
".venv\Scripts\python.exe" server.py --live --mirror %*
pause
