import os
import subprocess
import io

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