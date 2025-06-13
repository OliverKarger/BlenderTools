@echo off
title BlenderTools CLI

setlocal

:: Go into Addon Directory
cd "%APPDATA%\Blender Foundation\Blender\4.3\scripts\addons\blendertools"

:: Check if Python Virtual Environment exists
if exist ".venv" (
    :: If it exists, activate it
    call ".venv\Scripts\activate.bat" >nul 2>&1
) else (
    :: Create new 
    python -m venv .venv >nul 2>&1
    call ".venv\scripts\activate.bat" >nul 2>&1
)

:: Install Dependencies
pip install -r requirements.txt >nul 2>&1

:: Pass Arguments to CLI
python -m cli %*

endlocal