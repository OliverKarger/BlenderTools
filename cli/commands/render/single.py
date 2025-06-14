import os
import argparse
from cli.utils import blender

import bt_logger

logger = bt_logger.get_logger(__name__)

COMMAND_NAME = "single"
HELP = "Render a single blend file"


def setup(parser: argparse.ArgumentParser):
    parser.add_argument("-i", "--input", help="Input File", required=True)
    parser.add_argument("-o", "--output", help="Output File", required=True)
    parser.add_argument("-off", "--output-file-format", help="Output File Format", default="TIFF", required=False)
    parser.add_argument(
        "-f", "--override", help="Override Target File if exists", default=False, action="store_true", required=False
    )


def handle(args):
    input_file = args.input
    output_format = args.output_file_format.upper()
    filename_base = os.path.splitext(os.path.basename(input_file))[0]
    output_path = args.output.replace("{{filename}}", filename_base).replace("{{format}}", output_format.lower())

    if os.path.exists(output_path):
        if args.override:
            os.remove(output_path)
            logger.info(f"Output File {output_path} does already exists, deleting...")
        else:
            logger.warning(f"Output File {output_path} exists, skipping...")
            return

    if args.dry_run:
        logger.info("Skipping actual render")
        return

    blender.render(input_file, output_path, args.verbose, output_format)
