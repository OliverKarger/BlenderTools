import os
import subprocess
import io
import tempfile

from cli import constants

import bt_logger
logger = bt_logger.get_logger(__name__)

def invoke(opts: list[str]) -> bool:
    if not os.path.exists(constants.BLENDER_PATH):
        logger.fatal("Blender not found!")
        return False
    
    process_args = [constants.BLENDER_PATH] + opts

    logger.debug(f"Invoking Blender with Args: {process_args}")

    process = subprocess.Popen(
        process_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1)
    
    with io.TextIOWrapper(process.stdout, encoding="utf-8", errors="replace") as stdout:
        for line in stdout:
            formatted_line = f"BLENDER | {line}"
            logger.debug(formatted_line)

    if process.wait != 0:
        logger.fatal(f"Blender Error ({process.returncode})")
        return False

    return ("", True)

def render(file: str, verbose: bool, output: str | None) -> bool:
    if not os.path.exists(file):
        logger.error(f"File {file} does not exist!")
        return False

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
    
