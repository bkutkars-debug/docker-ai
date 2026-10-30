@echo off
title VideoTube AI Studio Launcher
echo ========================================================
echo       Starting VideoTube AI Studio (Meta AI Suite)
echo ========================================================
cd /d "%~dp0"

REM Check if Node.js VideoTube Server is running on port 8000
netstat -ano | findstr :8000 >nul
if %errorlevel% neq 0 (
    echo Starting VideoTube Server on http://localhost:8000 ...
    start /min "VideoTube Backend" cmd /c "node src/index.js"
    timeout /t 3 /nobreak >nul
) else (
    echo [OK] VideoTube Server is already running on http://localhost:8000
)

REM Check if Streamlit App is running on port 8501
netstat -ano | findstr :8501 >nul
if %errorlevel% neq 0 (
    echo Starting Streamlit App on http://localhost:8501 ...
    start /min "VideoTube Streamlit" cmd /c "streamlit run streamlit_app.py --server.headless true --server.port 8501"
    timeout /t 3 /nobreak >nul
) else (
    echo [OK] Streamlit App is already running on http://localhost:8501
)

echo ========================================================
echo Opening VideoTube AI Studio in your browser...
echo Permanent Link: http://localhost:8000
echo Streamlit Link: http://localhost:8501
echo ========================================================
start http://localhost:8000
timeout /t 2 /nobreak >nul
exit
