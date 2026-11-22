@echo off
setlocal
cd /d "%~dp0"
echo OmniPad PC - Install dependencies
py -3 --version >nul 2>&1
if errorlevel 1 (
  echo Python belum tersedia. Instal Python 3.11 atau 3.12 dari python.org lalu coba lagi.
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" py -3 -m venv .venv
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo Instalasi gagal. Periksa koneksi internet dan coba lagi.
  pause
  exit /b 1
)
echo Selesai. Buka START_PC.bat untuk memakai remote.
exit /b 0
