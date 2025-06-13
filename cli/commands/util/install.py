import argparse
import bt_logger

logger = bt_logger.get_logger(__name__)

COMMAND_NAME = "install"
HELP = "Installes CLI Script to be easily accessable using blender-cli"

from cli.utils.install import install_wrapper


def setup(parser: argparse.ArgumentParser):
    pass


def handle(args):
    install_wrapper()
