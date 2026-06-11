#!/bin/bash
echo -ne '\033]0;VX-NUKER v1.0.0\007'
clear

# Request root privileges
if [ "$EUID" -ne 0 ]; then
    echo "  [!] Requesting root privileges..."
    sudo "$0" "$@"
    exit $?
fi

if [ -f "dist/VX-NUKER" ]; then
    echo "  [+] Launching VX-NUKER (compiled)..."
    ./dist/VX-NUKER
else
    echo "  [*] Compiled build not found, running from source..."
    python3 main.py
fi
