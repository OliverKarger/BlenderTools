import argparse

COMMAND_NAME = "single"
HELP = "Render a single blend file"

def setup(parser: argparse.ArgumentParser):
    parser.add_argument("-i", "--input", help="Input File", required=True)
    parser.add_argument("-o", "--output", help="Output File", default="{{filename}}.{{format}}", required=True)
    parser.add_argument("-off", "--output-file-format", help="Output File Format", default="TIFF", required=False)

def handle(args):
    pass
