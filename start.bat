@echo off
title VX-NUKER v1.0.0
color 04
cls

:: Request admin elevation
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo  [!] Requesting Administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

if exist "dist\VX-NUKER.exe" (
    echo  [+] Launching VX-NUKER (compiled)...
    start "" "dist\VX-NUKER.exe"
) else (
    echo  [*] Compiled build not found, running from source...
    python main.py
)
pause
