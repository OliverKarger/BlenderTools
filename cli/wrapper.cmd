@echo off
setlocal

REM Path to Blender executable
set BLENDER_EXE="C:\Program Files\Blender Foundation\Blender 4.3\blender.exe"

REM Path to your CLI entry point
set SCRIPT_PATH=%APPDATA%\Blender Foundation\Blender\4.3\scripts\addons\blendertools\cli\__main__.py

REM Run Blender in background and pass CLI args after "--"
%BLENDER_EXE% --background --python "%SCRIPT_PATH%" -- %*

endlocal
