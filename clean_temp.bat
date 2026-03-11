@echo off
REM ============================================
REM Clean PyInstaller Temp Files
REM ============================================

echo.
echo ================================================
echo  Cleaning PyInstaller Temporary Files
echo ================================================
echo.
echo This will delete all _MEI* folders in TEMP directory
echo.
pause

echo.
echo Cleaning temporary files...
echo.

cd /d %TEMP%

REM Count _MEI folders
set count=0
for /d %%i in (_MEI*) do set /a count+=1

if %count% equ 0 (
    echo No _MEI folders found.
    echo.
    goto :end
)

echo Found %count% _MEI folder(s)
echo.

REM Delete all _MEI folders
for /d %%i in (_MEI*) do (
    echo Deleting: %%i
    rmdir /s /q "%%i" 2>nul
    if exist "%%i" (
        echo Warning: Could not delete %%i
        echo Try closing all programs and run this script again
    ) else (
        echo Success: %%i deleted
    )
)

echo.
echo ================================================
echo  Cleanup Complete
echo ================================================
echo.
echo Please try running PDFQRCodeCompare.exe again
echo.

:end
pause
