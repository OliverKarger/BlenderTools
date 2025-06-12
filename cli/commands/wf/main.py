import argparse

COMMAND_NAME = "wf"
HELP = "Blender Python Workflow"

def setup(parser: argparse.ArgumentParser):
    parser.add_argument("-p", "--python-file", help="Name of Python File to execute", required=True)
    parser.add_argument("-f", "--file", help="Path to Blender File", required=False)
    parser.add_argument("-fp", "--file-pattern", help="File Pattern for Blender Files", required=False)

def handle(args):
    pass
