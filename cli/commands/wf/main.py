import argparse
import os
import glob

from cli.utils import blender
import bt_logger

logger = bt_logger.get_logger(__name__)

COMMAND_NAME = "wf"
HELP = "Blender Python Workflow"

def setup(parser: argparse.ArgumentParser):
    parser.add_argument("-p", "--python-file", help="Name of Python File to execute", required=True)
    parser.add_argument("-f", "--file", help="Path to Blender File", required=False)
    parser.add_argument("-fp", "--file-pattern", help="File Pattern for Blender Files", required=False)

def handle(args: list[str]):
    if args.file is None and args.file_pattern is None:
        logger.error("Either specify --file or --file-pattern")
        return

    if args.file and not os.path.exists(args.file):
        logger.error(f"File '{args.file}' does not exist!")
        return

    if not os.path.exists(args.python_file):
        logger.error(f"Python script '{args.python_file}' does not exist!")
        return

    if args.file:
        # Single file render

        if args.verbose:
            logger.info(f"Processing: {args.file}")

        if not args.dry_run:
            command = ["-b", args.file, "-y", "--python", args.python_file]
            blender.invoke(command, verbose=args.verbose)
        return

    if args.file_pattern:
        # Expand pattern and sort files for consistency
        matched_files = sorted(glob.glob(args.file_pattern, recursive=True))
        
        if not matched_files:
            logger.error(f"No files found matching pattern '{args.file_pattern}'")
            return

        for filepath in matched_files:
            if not filepath.endswith(".blend"):
                continue

            if args.verbose:
                logger.info(f"Processing: {filepath}")

            if not args.dry_run:
                command = ["-b", filepath, "-y", "--python", args.python_file]
                blender.invoke(command, verbose=args.verbose)
