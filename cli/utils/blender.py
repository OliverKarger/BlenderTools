import os
import subprocess
import io
import tempfile

from cli import constants

def invoke(opts: list[str], verbose: bool) -> tuple[str, bool]:
    if not os.path.exists(constants.BLENDER_PATH):
        return ("Blender not found!", False)
    
    process_args = [constants.BLENDER_PATH] + opts

    if verbose:
        print(f"[DEBUG] Invoking Blender with Args: {process_args}")

    process = subprocess.Popen(
        process_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1)
    
    with io.TextIOWrapper(process.stdout, encoding="utf-8", errors="replace") as stdout:
        for line in stdout:
            formatted_line = f"BLENDER | {line}"
            print(formatted_line, end='', flush=True)

    if process.wait != 0:
        return (process.returncode, False)

    return ("", True)

def render(file: str, verbose: bool, output: str | None) -> tuple[str, bool]:
    if not os.path.exists(file):
        return (f"File {file} does not exist", False)
    
    # Create Temporary Blender Script
    temp_dir = tempfile.gettempdir()
    script_path = os.path.join(temp_dir, "blender_render.py")

    if os.path.exists(script_path):
        os.remove(script_path)

    with open(script_path, "w") as f:
        f.write("import bpy\n")
        f.write("bpy.ops.render.render(write_still=True)\n")

    args = [constants.BLENDER_PATH, "-b", file, "-y", "--python", script_path]

    if output is not None:
        args += ["-o", output]

    result = invoke(args, verbose)
    if result[1] == False:
        return result
    
