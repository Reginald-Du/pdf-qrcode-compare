@echo off
REM ============================================
REM Visual C++ Redistributable Auto-Installer
REM ============================================

echo.
echo ================================================
echo  Visual C++ Redistributable Auto-Installer
echo ================================================
echo.
echo This script will download and install required
echo Visual C++ Redistributable packages.
echo.
pause

REM Create temp directory
set TEMP_DIR=%TEMP%\vcredist_install
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"
cd /d "%TEMP_DIR%"

echo.
echo [1/3] Downloading Visual C++ 2015-2022 (x64)...
echo.

REM Download VC++ 2015-2022
powershell -Command "& {Invoke-WebRequest -Uri 'https://aka.ms/vs/17/release/vc_redist.x64.exe' -OutFile 'vc_redist_2015_2022_x64.exe'}"

if not exist "vc_redist_2015_2022_x64.exe" (
    echo ERROR: Failed to download VC++ 2015-2022
    echo Please download manually from: https://aka.ms/vs/17/release/vc_redist.x64.exe
    pause
    exit /b 1
)

echo.
echo [2/3] Installing Visual C++ 2015-2022 (x64)...
echo Please wait...
echo.

REM Install with repair option
start /wait vc_redist_2015_2022_x64.exe /install /quiet /norestart

if %errorlevel% equ 0 (
    echo SUCCESS: Visual C++ 2015-2022 installed successfully!
) else if %errorlevel% equ 3010 (
    echo SUCCESS: Visual C++ 2015-2022 installed (restart required)
) else (
    echo WARNING: Installation returned code %errorlevel%
    echo You may need to run the installer manually.
)

echo.
echo [3/3] Cleaning up...
cd /d %TEMP%
rmdir /s /q "%TEMP_DIR%" 2>nul

echo.
echo ================================================
echo  Installation Complete!
echo ================================================
echo.
echo IMPORTANT: Please restart your computer now!
echo.
echo After restart, try running PDFQRCodeCompare.exe again.
echo.
echo If you still get errors, please refer to:
echo https://github.com/Reginald-Du/pdf-qrcode-compare/blob/main/CRITICAL_FIX.md
echo.
pause

REM Ask to restart
echo.
choice /C YN /M "Do you want to restart now"
if %errorlevel% equ 1 (
    echo Restarting computer...
    shutdown /r /t 10 /c "Restarting to complete Visual C++ installation"
    echo.
    echo Computer will restart in 10 seconds...
    echo Press Ctrl+C to cancel
    pause
)
