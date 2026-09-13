@echo off
setlocal
title Local LLM Chat - Ollama

rem Switch to this script's own folder first (handles non-ASCII paths safely).
cd /d "%~dp0"

set "OLLAMA=%LOCALAPPDATA%\Programs\Ollama\ollama.exe"
set "PY=venv\Scripts\python.exe"
set "URL=http://127.0.0.1:5000"
set "OLLAMA_MODEL=qwen2.5-coder:7b"

echo.
echo  ============================================
echo    Local LLM Chat  -  one-click start
echo  ============================================
echo.

rem ---- 1. make sure Ollama is running (port 11434) ----
curl -s -m 2 http://localhost:11434/api/version >nul 2>&1
if errorlevel 1 (
    echo  [1/3] Starting Ollama service...
    start "" "%OLLAMA%" serve
    ping -n 6 127.0.0.1 >nul
) else (
    echo  [1/3] Ollama service already running
)

rem ---- 2. make sure chat server is running (port 5000) ----
powershell -NoProfile -Command "try{(New-Object Net.Sockets.TcpClient).Connect('127.0.0.1',5000);exit 0}catch{exit 1}"
if errorlevel 1 (
    echo  [2/3] Starting chat server...
    start "LLM Chat Server" /min "%PY%" "-u" "chat_server.py"
    ping -n 8 127.0.0.1 >nul
) else (
    echo  [2/3] Chat server already running
)

rem ---- 3. open browser ----
echo  [3/3] Opening browser...
start "" "%URL%"

echo.
echo  Ready: %URL%   (first query may be slow while index builds)
echo.
ping -n 4 127.0.0.1 >nul
endlocal
