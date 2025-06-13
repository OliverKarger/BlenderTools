# CLI Workflow Examples

## Update Object in Blender File

### Objective
This example will update the Light Source Intensity/Energy/Strength to 1000 using BlenderTools' Workflow System

### Walkthrough

Run the CLI Command:

```
"%APPDATA%\Blender Foundation\Blender\4.3\scripts\addons\blendertools\cli\wrapper.cmd" ^
    wf ^
    -p "%APPDATA%\Blender Foundation\Blender\4.3\scripts\addons\blendertools\cli\examples\update_light.py" ^
    -f "%APPDATA%\Blender Foundation\Blender\4.3\scripts\addons\blendertools\cli\examples\example.blend"
```

## Render Blender File

### Objective
Render a single Blender File using BlenderTools' Render System

### Walkthrough

Run the CLI Command:

```
"%APPDATA%\Blender Foundation\Blender\4.3\scripts\addons\blendertools\cli\wrapper.cmd" ^
    render single ^
    -i "%APPDATA%\Blender Foundation\Blender\4.3\scripts\addons\blendertools\cli\examples\example.blend" ^
    -o "C:\tmp\test.tiff" ^
    -off "TIFF"
```