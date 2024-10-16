@echo off
:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and add it to your PATH.
    pause
    exit /b
)

:: Change to the directory where your script is located
cd /d "%~dp0"

:: Run the Python script
python AdbAndFastbootIn10secounds_1.0.2Fix-2_Installer.py

:: Pause to keep the window open
pause
