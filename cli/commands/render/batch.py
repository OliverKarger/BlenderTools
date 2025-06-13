import argparse
import os
import glob
from cli.utils import blender

import bt_logger
logger = bt_logger.get_logger(__name__)

COMMAND_NAME = "batch"
HELP = "Batch Renders Files"

def setup(parser: argparse.ArgumentParser):
    parser.add_argument("-i", "--input", help="Input Path", default=os.getcwd(), required=True)
    parser.add_argument("-o", "--output", help="Output Path", default=os.path.join(os.getcwd(), "renders"), required=False)
    parser.add_argument("-off", "--output-file-format", help="Output File Format", default="TIFF", required=False)
    parser.add_argument("-if", "--input-format", help="Input File Format", default="*.blend", required=False)
    parser.add_argument("-of", "--output-format", help="Output File Format", default="{{filename}}.{{format}}", required=False)

def handle(args):
    input_dir = args.input
    output_dir = args.output
    input_pattern = args.input_format
    output_template = args.output_format  # could be None
    output_file_format = args.output_file_format.upper()

    if not os.path.exists(input_dir):
        logger.error(f"Input path '{input_dir}' does not exist.")
        return

    os.makedirs(output_dir, exist_ok=True)

    # Find all matching .blend files
    search_pattern = os.path.join(input_dir, "**", input_pattern)
    blend_files = sorted(glob.glob(search_pattern, recursive=True))

    if not blend_files:
        logger.error(f"No files found matching pattern '{input_pattern}' in '{input_dir}'")
        return

    for blend_file in blend_files:
        if not blend_file.endswith(".blend"):
            continue

        # If output template was explicitly provided, render to output path
        if output_template:
            filename_base = os.path.splitext(os.path.basename(blend_file))[0]
            output_filename = output_template.replace("{{filename}}", filename_base).replace("{{format}}", output_file_format.lower())
            output_path = os.path.join(output_dir, output_filename)
        else:
            output_path = None  # Fall back to Blender's internal settings

        if args.verbose:
            if output_path:
                logger.info(f"Rendering '{blend_file}' → '{output_path}' as {output_file_format}")
            else:
                logger.info(f"Rendering '{blend_file}' using Blender's internal output path")

        if args.dry_run:
            logger.info(f"Skipping actual render for '{blend_file}'")
            continue

        blender.render(blend_file, verbose=args.verbose, output=output_path)
