import os
import subprocess
import io
import tempfile

from cli import constants

import bt_logger

logger = bt_logger.get_logger(__name__)


def invoke(opts: list[str], verbose: bool = False) -> bool:
    """
    Invokes the Blender application with specified options and optionally provides verbose
    output during its execution.

    Parameters
    ----------
    opts : list[str]
        List of command-line arguments to pass to the Blender application.
    verbose : bool, optional
        If True, enables verbose logging of Blender's execution output. Defaults to False.

    Returns
    -------
    bool
        True if Blender was successfully invoked and executed; otherwise, False.

    Raises
    ------
    None
    """
    if not os.path.exists(constants.BLENDER_PATH):
        logger.fatal("Blender not found!")
        return False

    process_args = [constants.BLENDER_PATH] + opts

    logger.debug(f"Invoking Blender with Args: {process_args}")

    process = subprocess.Popen(process_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)

    if verbose:
        with io.TextIOWrapper(process.stdout, encoding="utf-8", errors="replace") as stdout:
            for line in stdout:
                formatted_line = f"BLENDER | {line.rstrip()}"
                logger.debug(formatted_line)

    if process.wait != 0 and process.returncode is not None:
        logger.fatal(f"Blender Error ({process.returncode})")
        return False

    return ("", True)


def render(file: str, output: str, verbose: bool = False, output_format: str = "TIFF") -> bool:
    """
    Renders a Blender file using the specified output format and saves it to the given location.

    Parameters:
    file: str
        The path to the Blender file that will be rendered.
    output: str
        The path where the rendered image will be saved.
    verbose: bool, optional
        Whether to enable verbose output during the rendering process. Default is False.
    output_format: str, optional
        The desired format of the output image. Default is "TIFF".

    Returns:
    bool
        True if the rendering process is successful, otherwise False.
    """
    if not os.path.exists(file):
        logger.error(f"Blender File {file} does not exist!")
        return False

    output_dir = os.path.dirname(output)
    os.makedirs(output_dir, exist_ok=True)

    # Create Temporary Blender Script
    temp_dir = tempfile.gettempdir()
    script_path = os.path.join(temp_dir, "blender_render.py")

    if os.path.exists(script_path):
        os.remove(script_path)

    with open(script_path, "w") as f:
        f.write("import bpy\n")
        f.write(f'bpy.context.scene.render.image_settings.file_format="{output_format}"\n')
        f.write(f'bpy.context.scene.render.filepath = r"{output}"\n')
        f.write("bpy.ops.render.render(write_still=True)\n")

    args = ["-b", file, "-y", "--python", script_path, "-o", output]

    logger.info(f"Rendering '{file}' to '{output}'")
    result = invoke(args, verbose)

    os.remove(script_path)

    return result
