import argparse
import os
import glob
import cli.commands.render.single as single_render_cmd
import bt_logger

logger = bt_logger.get_logger(__name__)

COMMAND_NAME = "batch"
HELP = "Batch Renders Files"


def setup(parser: argparse.ArgumentParser):
    parser.add_argument("-i", "--input", help="Input Path", default=os.getcwd(), required=True)
    parser.add_argument(
        "-o", "--output", help="Output Path", default=os.path.join(os.getcwd(), "renders"), required=True
    )
    parser.add_argument("-off", "--output-file-format", help="Output File Format", default="TIFF", required=False)
    parser.add_argument("-if", "--input-format", help="Input File Format", default="*.blend", required=False)
    parser.add_argument(
        "-of", "--output-format", help="Output Filename Template", default="{{filename}}.{{format}}", required=False
    )
    parser.add_argument(
        "-f", "--override", help="Override Target File if exists", default=False, action="store_true", required=False
    )


def handle(args):
    input_dir = args.input
    output_dir = args.output
    input_pattern = args.input_format
    output_template = args.output_format
    output_file_format = args.output_file_format.upper()

    search_pattern = os.path.join(input_dir, "**", input_pattern)
    blend_files = sorted(glob.glob(search_pattern, recursive=True))

    if not blend_files:
        logger.error(f"No files found matching pattern '{input_pattern}' in '{input_dir}'")
        return

    for blend_file in blend_files:
        if not blend_file.endswith(".blend"):
            continue

        filename_base = os.path.splitext(os.path.basename(blend_file))[0]
        output_filename = output_template.replace("{{filename}}", filename_base).replace(
            "{{format}}", output_file_format.lower()
        )
        full_output_path = os.path.join(output_dir, output_filename)

        single_args = argparse.Namespace(
            input=blend_file,
            output=full_output_path,
            output_file_format=output_file_format,
            override=args.override,
            dry_run=args.dry_run,
            verbose=args.verbose,
        )

        single_render_cmd.handle(single_args)
