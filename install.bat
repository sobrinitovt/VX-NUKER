@echo off
title VX-NUKER - Installer
color 04
cls

:: Request admin elevation
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo  [!] Requesting Administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo.
echo  ============================================================
echo    VX-NUKER  -  Installation Script
echo  ============================================================
echo.
echo  [*] Checking Python installation...
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [-] Python is not installed or not in PATH.
    echo  [-] Download Python 3.10+ from https://python.org
    echo.
    pause
    exit /b 1
)

echo  [+] Python found.
echo.
echo  [*] Installing runtime dependencies...
echo.

pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo  [-] Runtime dependencies installation failed.
    pause
    exit /b 1
)

echo.
echo  [*] Installing build tools (PyArmor + PyInstaller)...
echo.

pip install pyarmor pyinstaller

if %errorlevel% neq 0 (
    echo.
    echo  [-] Build tools installation failed.
    pause
    exit /b 1
)

echo.
echo  ============================================================
echo  [+] Installation complete.
echo  [+] Run build.bat to compile the executable.
echo  [+] Run start.bat to launch VX-NUKER.
echo  ============================================================
echo.
pause
