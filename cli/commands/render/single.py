import os
import argparse
from cli.utils import blender

import bt_logger

logger = bt_logger.get_logger(__name__)

COMMAND_NAME = "single"
HELP = "Render a single blend file"


def setup(parser: argparse.ArgumentParser):
    parser.add_argument("-i", "--input", help="Input File", required=True)
    parser.add_argument(
        "-o", "--output", help="Output File (optional, defaults to Blender's internal path)", required=True
    )
    parser.add_argument("-off", "--output-file-format", help="Output File Format", default="TIFF", required=False)


def handle(args):
    input_file = args.input
    output_format = args.output_file_format.upper()

    if not os.path.exists(input_file):
        logger.error(f"Input file '{input_file}' does not exist.")
        return

    output_path = None

    if args.output:
        filename_base = os.path.splitext(os.path.basename(input_file))[0]
        output_path = args.output.replace("{{filename}}", filename_base).replace("{{format}}", output_format.lower())

    if output_path:
        logger.info(f"Rendering '{input_file}' to '{output_path}' as {output_format}")
    else:
        logger.info(f"Rendering '{input_file}' using Blender's internal output path")

    if args.dry_run:
        logger.info("Skipping actual render")
        return

    blender.render(input_file, verbose=args.verbose, output=output_path, output_format=output_format)
