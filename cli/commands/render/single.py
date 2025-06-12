import os
import argparse
from cli.utils import blender

COMMAND_NAME = "single"
HELP = "Render a single blend file"

def setup(parser: argparse.ArgumentParser):
    parser.add_argument("-i", "--input", help="Input File", required=True)
    parser.add_argument("-o", "--output", help="Output File (optional, defaults to Blender's internal path)", required=False)
    parser.add_argument("-off", "--output-file-format", help="Output File Format", default="TIFF", required=False)

def handle(args):
    input_file = args.input
    output_format = args.output_file_format.upper()

    if not os.path.exists(input_file):
        print(f"[ERROR] Input file '{input_file}' does not exist.")
        return

    output_path = None

    if args.output:
        filename_base = os.path.splitext(os.path.basename(input_file))[0]
        output_path = args.output.replace("{{filename}}", filename_base).replace("{{format}}", output_format.lower())

    if args.verbose:
        if output_path:
            print(f"[INFO] Rendering '{input_file}' to '{output_path}' as {output_format}")
        else:
            print(f"[INFO] Rendering '{input_file}' using Blender's internal output path")

    if args.dry_run:
        print("[DRY RUN] Skipping actual render")
        return

    result = blender.render(input_file, verbose=args.verbose, output=output_path)

    if not result[1]:
        print(f"[ERROR] Render failed: {result[0]}")
    elif args.verbose:
        print("[SUCCESS] Render completed.")
