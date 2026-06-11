@echo off
title VX-NUKER - Build System
color 04
cls

echo.
echo  ============================================================
echo    VX-NUKER  -  Build System (PyArmor + PyInstaller)
echo  ============================================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [-] Python not found in PATH.
    pause
    exit /b 1
)

:: Install build dependencies
echo  [*] Installing build dependencies...
pip install pyarmor pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo  [-] Failed to install build tools.
    pause
    exit /b 1
)
echo  [+] Build tools ready.
echo.

:: Clean previous builds
echo  [*] Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "obfuscated" rmdir /s /q "obfuscated"
echo  [+] Clean.
echo.

:: Obfuscate with PyArmor
echo  [*] Obfuscating main.py with PyArmor...
pyarmor gen --output obfuscated main.py
if %errorlevel% neq 0 (
    echo  [-] PyArmor obfuscation failed.
    pause
    exit /b 1
)
echo  [+] Obfuscation complete.
echo.

:: Build with PyInstaller
echo  [*] Building executable with PyInstaller...
pyinstaller ^
    --onefile ^
    --console ^
    --name "VX-NUKER" ^
    --icon "icon.ico" ^
    --manifest "app.manifest" ^
    --hidden-import=discord ^
    --hidden-import=discord.ext.commands ^
    --hidden-import=discord.ext ^
    --hidden-import=discord.types ^
    --hidden-import=discord.ui ^
    --hidden-import=discord.webhook ^
    --hidden-import=discord.app_commands ^
    --hidden-import=aiohttp ^
    --hidden-import=aiohttp.connector ^
    --hidden-import=aiohttp.client ^
    --hidden-import=aiohttp.web ^
    --hidden-import=aiohttp.hdrs ^
    --hidden-import=aiohttp.typedefs ^
    --hidden-import=aiohttp.client_reqrep ^
    --hidden-import=multidict ^
    --hidden-import=yarl ^
    --hidden-import=async_timeout ^
    --hidden-import=aiosignal ^
    --hidden-import=frozenlist ^
    --hidden-import=charset_normalizer ^
    --hidden-import=attrs ^
    --hidden-import=colorama ^
    --hidden-import=json ^
    --hidden-import=asyncio ^
    --hidden-import=asyncio.events ^
    --hidden-import=asyncio.base_events ^
    --hidden-import=asyncio.proactor_events ^
    --hidden-import=asyncio.windows_events ^
    --hidden-import=asyncio.selector_events ^
    --hidden-import=urllib ^
    --hidden-import=urllib.request ^
    --hidden-import=webbrowser ^
    --hidden-import=shutil ^
    --hidden-import=re ^
    --hidden-import=datetime ^
    --hidden-import=certifi ^
    --hidden-import=ssl ^
    --hidden-import=_ssl ^
    --add-data "icon.ico;." ^
    --uac-admin ^
    "obfuscated/main.py"

if %errorlevel% neq 0 (
    echo  [-] PyInstaller build failed.
    pause
    exit /b 1
)

echo.
echo  ============================================================
echo  [+] Build complete!
echo  [+] Executable: dist\VX-NUKER.exe
echo  [+] The executable requires Administrator privileges.
echo  ============================================================
echo.

:: Cleanup intermediate files
if exist "obfuscated" rmdir /s /q "obfuscated"
if exist "build" rmdir /s /q "build"
if exist "VX-NUKER.spec" del /f "VX-NUKER.spec"

pause
