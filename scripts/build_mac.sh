#!/bin/bash
set -e

# Ensure we are in the project root
cd "$(dirname "$0")/.."

# Activate venv
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found! Please create it first."
    exit 1
fi

# Install PyInstaller if missing
if ! pip show pyinstaller > /dev/null; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

# Check for UPX (Ultimate Packer for eXecutables)
if ! command -v upx &> /dev/null; then
    echo "WARNING: UPX is not installed or not in PATH."
    echo "To significantly reduce file size, install UPX: brew install upx"
    echo "PyInstaller will proceed without UPX compression."
else
    echo "UPX found. Binary compression enabled."
fi

# Clean previous build
rm -rf build dist

# Use local cache directory to avoid permission issues
export PYINSTALLER_CONFIG_DIR="$(pwd)/.pyinstaller_cache"

# Build using .spec
echo "Building macOS .app (Optimized)..."
# --noconfirm overwrites output directory without asking
# Removed --clean to avoid permission errors on macOS cache
pyinstaller --noconfirm main.spec

# Create DMG (Optional, requires create-dmg)
if command -v create-dmg &> /dev/null; then
    echo "Creating DMG..."
    mkdir -p dist/dmg
    create-dmg \
      --volname "PDF QR Compare" \
      --window-pos 200 120 \
      --window-size 800 400 \
      --icon-size 100 \
      --icon "PDFQRCodeCompare.app" 200 190 \
      --hide-extension "PDFQRCodeCompare.app" \
      --app-drop-link 600 185 \
      "dist/dmg/PDFQRCodeCompare.dmg" \
      "dist/PDFQRCodeCompare.app"
else
    echo "create-dmg not found. Creating ZIP archive instead."
    cd dist
    zip -r "PDFQRCodeCompare-macOS.zip" "PDFQRCodeCompare.app"
    cd ..
fi

echo "Build complete! Check dist/ folder."
