#!/data/data/com.termux/files/usr/bin/bash
clear
echo ""
echo "  ============================================================"
echo "    VX-NUKER  -  Termux Installer"
echo "  ============================================================"
echo ""
echo "  [*] Updating packages..."
echo ""
pkg update -y && pkg upgrade -y

echo "  [*] Installing Python..."
echo ""
pkg install -y python python-pip

echo "  [*] Installing dependencies..."
echo ""
pip install discord.py aiohttp colorama

echo ""
echo "  ============================================================"
echo "  [+] Installation complete!"
echo "  [+] Run: python main.py"
echo "  ============================================================"
echo ""
