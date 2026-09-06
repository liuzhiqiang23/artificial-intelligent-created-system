@echo off
setlocal
title Local LLM Chat - Ollama

rem Use this script's own folder as the project root (handles non-ASCII paths).
set "ROOT=%~dp0"
set "OLLAMA=%LOCALAPPDATA%\Programs\Ollama\ollama.exe"
set "PY=%ROOT%venv\Scripts\python.exe"
set "URL=http://127.0.0.1:5000"

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
    timeout /t 6 /nobreak >nul
) else (
    echo  [1/3] Ollama service already running
)

rem ---- 2. make sure chat server is running (port 5000) ----
powershell -NoProfile -Command "try{(New-Object Net.Sockets.TcpClient).Connect('127.0.0.1',5000);exit 0}catch{exit 1}"
if errorlevel 1 (
    echo  [2/3] Starting chat server...
    start "LLM Chat Server" /min cmd /c "set PYTHONIOENCODING=utf-8 && cd /d "%ROOT%" && "%PY%" -u chat_server.py"
    timeout /t 5 /nobreak >nul
) else (
    echo  [2/3] Chat server already running
)

rem ---- 3. open browser ----
echo  [3/3] Opening browser...
start "" "%URL%"

echo.
echo  Ready: %URL%
echo  Note: the first "search local" request may take a few seconds.
echo.
timeout /t 5 /nobreak >nul
endlocal
