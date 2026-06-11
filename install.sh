#!/bin/bash

clear

# Request root privileges
if [ "$EUID" -ne 0 ]; then
    echo "  [!] Requesting root privileges..."
    sudo "$0" "$@"
    exit $?
fi

echo ""
echo "  ============================================================"
echo "    VX-NUKER  -  Installation Script"
echo "  ============================================================"
echo ""
echo "  [*] Checking Python installation..."
echo ""

if ! command -v python3 &> /dev/null; then
    echo "  [-] Python3 is not installed."
    echo "  [-] Install it with: sudo apt install python3 python3-pip"
    exit 1
fi

echo "  [+] Python3 found."
echo ""
echo "  [*] Installing runtime dependencies..."
echo ""

pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "  [-] Runtime dependencies installation failed."
    exit 1
fi

echo ""
echo "  [*] Installing build tools (PyArmor + PyInstaller)..."
echo ""

pip3 install pyarmor pyinstaller

if [ $? -ne 0 ]; then
    echo ""
    echo "  [-] Build tools installation failed."
    exit 1
fi

echo ""
echo "  ============================================================"
echo "  [+] Installation complete."
echo "  [+] Run build.bat (Windows) or manually build on Linux."
echo "  [+] Run ./start.sh to launch VX-NUKER."
echo "  ============================================================"
echo ""
