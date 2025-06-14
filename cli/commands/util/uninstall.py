import argparse
import bt_logger
from cli.utils.install import uninstall_wrapper

logger = bt_logger.get_logger(__name__)

COMMAND_NAME = "uninstall"
HELP = "Uninstalles CLI Script"


def setup(parser: argparse.ArgumentParser):
    pass


def handle(args):
    uninstall_wrapper()
