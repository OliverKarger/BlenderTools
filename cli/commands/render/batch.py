import argparse
import os

COMMAND_NAME = "batch"
HELP = "Batch Renders Files"

def setup(parser: argparse.ArgumentParser):
    parser.add_argument("-i", "--input", help="Input Path", default=os.getcwd(), required=True)
    parser.add_argument("-o", "--output", help="Output Path", default=os.path.join(os.getcwd(), "renders"), required=True)
    parser.add_argument("-off", "--output-file-format", help="Output File Format", default="TIFF", required=False)
    parser.add_argument("-if", "--input-format", help="Input File Format", default="*.blend", required=False)
    parser.add_argument("-of", "--output-format", help="Output File Format", default="{{filename}}.{{format}}", required=False)

def handle(args):
    pass
