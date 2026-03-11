@echo off
REM Windows Build Script with Enhanced Compatibility
REM This version includes VC++ runtime bundling for better compatibility

cd /d "%~dp0\.."

if not exist venv (
    echo Virtual environment not found! Please run 'python -m venv venv' and install requirements.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM Ensure PyInstaller is installed
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo ========================================
echo Building Windows Executable (Enhanced)
echo ========================================

REM Build with additional options for better compatibility
pyinstaller ^
    --clean ^
    --noconfirm ^
    --onedir ^
    --windowed ^
    --name "PDFQRCodeCompare" ^
    --icon "resources/icon.ico" ^
    --add-data "resources;resources" ^
    --hidden-import "numpy.core._multiarray_umath" ^
    --hidden-import "numpy.random.common" ^
    --hidden-import "numpy.random.bounded_integers" ^
    --hidden-import "numpy.random.entropy" ^
    --hidden-import "zxingcpp" ^
    --hidden-import "shapely" ^
    --hidden-import "shapely.geometry" ^
    --collect-all "numpy" ^
    --collect-all "zxingcpp" ^
    --collect-binaries "shapely" ^
    --exclude-module "tkinter" ^
    --exclude-module "matplotlib" ^
    --exclude-module "scipy" ^
    --exclude-module "pandas" ^
    main.py

if %errorlevel% neq 0 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build complete!
echo ========================================
echo.
echo Output: dist\PDFQRCodeCompare\PDFQRCodeCompare.exe
echo.
echo Creating ZIP archive...
cd dist
powershell Compress-Archive -Force -Path PDFQRCodeCompare -DestinationPath PDFQRCodeCompare-Windows-Fixed.zip
cd ..

echo.
echo ZIP created: dist\PDFQRCodeCompare-Windows-Fixed.zip
echo.
echo IMPORTANT: Users need to install Visual C++ Redistributable:
echo https://aka.ms/vs/17/release/vc_redist.x64.exe
echo.
pause
