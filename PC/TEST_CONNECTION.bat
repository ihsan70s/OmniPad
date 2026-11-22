@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" call SETUP_PC.bat
if errorlevel 1 exit /b 1
echo OmniPad DRY RUN - hanya menguji koneksi, tanpa mengontrol PC.
".venv\Scripts\python.exe" server.py %*
pause
