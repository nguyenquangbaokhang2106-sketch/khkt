@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Open index.html directly in your browser.
  pause
  exit /b 1
)
python serve.py
if errorlevel 1 pause
