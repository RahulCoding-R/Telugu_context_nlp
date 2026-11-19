
@echo off
title Telugu AI Launcher

cd /d "%~dp0"

echo =====================================
echo       STARTING TELUGU AI
echo =====================================

echo Starting IndicXlit...
start "IndicXlit - Port 5001" /D "%~dp0" "%~dp0xlit_env\Scripts\python.exe" "%~dp0backend\xlit_service.py"

timeout /t 5 /nobreak >nul

echo Starting FastAPI...
start "FastAPI - Port 8000" /D "%~dp0" "%~dp0.venv\Scripts\python.exe" -m uvicorn backend.main:app --host 127.0.0.1 --port 8000

timeout /t 10 /nobreak >nul

echo Opening website...
start "" "http://127.0.0.1:8000/"

echo.
echo Startup commands sent.
pause
