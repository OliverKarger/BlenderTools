import argparse
import bt_logger

logger = bt_logger.get_logger(__name__)

COMMAND_NAME = "uninstall"
HELP = "Uninstalles CLI Script"

from cli.utils.install import uninstall_wrapper


def setup(parser: argparse.ArgumentParser):
    pass


def handle(args):
    uninstall_wrapper()
