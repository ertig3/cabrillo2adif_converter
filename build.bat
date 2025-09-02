@echo off
echo Cabrillo2ADIF Converter Build Script
echo Date: 2025-09-02 19:23:22
echo User: ertig3

python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found, trying py command
    py --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python not installed
        pause
        exit /b 1
    )
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)

echo Installing PyInstaller...
%PYTHON_CMD% -m pip install pyinstaller

echo Cleaning build directories...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

echo Building executable...
if exist icon.ico (
    %PYTHON_CMD% -m PyInstaller --onefile --windowed --icon=icon.ico --name="Cabrillo2ADIF_Converter_v0.9" main.py
) else (
    %PYTHON_CMD% -m PyInstaller --onefile --windowed --name="Cabrillo2ADIF_Converter_v0.9" main.py
)

if exist dist\Cabrillo2ADIF_Converter_v0.9.exe (
    echo Build successful
    dir dist\Cabrillo2ADIF_Converter_v0.9.exe
    echo EXE location: dist\Cabrillo2ADIF_Converter_v0.9.exe
) else (
    echo Build failed
)

pause