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
    -f "%APPDATA%\Blender Foundation\Blender\4.3\scripts\addons\blendertools\cli\examples\example1.blend"
```

## Render Blender File

### Objective
Render a single Blender File using BlenderTools' Render System

### Walkthrough

Run the CLI Command:

```
"%APPDATA%\Blender Foundation\Blender\4.3\scripts\addons\blendertools\cli\wrapper.cmd" ^
    render single ^
    -i "%APPDATA%\Blender Foundation\Blender\4.3\scripts\addons\blendertools\cli\examples\example1.blend" ^
    -o "C:\tmp\test.tiff" ^
    -off "TIFF"
```

## Render multible Blender Files

### Objective
Render multible Blender Files using BlenderTools' Batch Render System

### Walkthrough

Run the CLI Command

```
"%APPDATA%\Blender Foundation\Blender\4.3\scripts\addons\blendertools\cli\wrapper.cmd" ^
    render batch ^
    -i "%APPDATA%\Blender Foundation\Blender\4.3\scripts\addons\blendertools\cli\examples" ^
    -if "*.blend" ^
    -o "C:\temp" ^
    -of "{{filename}}.tiff" ^
    -off "TIFF"
```