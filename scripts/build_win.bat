@echo off
cd /d "%~dp0\.."

if not exist venv (
    echo Virtual environment not found! Please run 'python -m venv venv' and install requirements.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo Building Windows Executable...
pyinstaller --clean main.spec

echo Build complete!
echo You can find the executable in dist\PDFQRCodeCompare\PDFQRCodeCompare.exe
pause
