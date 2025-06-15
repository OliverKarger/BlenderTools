import logging
import os

from . import parser
from . import bt_logger

logger = bt_logger.get_logger(__name__)


def main():
    """
    Main entry point for the application.

    This function configures the logging level, parses command-line arguments,
    and executes the appropriate handler function if defined.
    If no handler function is defined or callable, an error message is printed.

    Raises:
        AttributeError: If `args` lacks the `handler` attribute but this is not callable.

    """
    bt_logger.global_log_level = logging.CRITICAL

    logger.debug(f"Running in {os.getcwd()}")

    args = parser.parse()

    if hasattr(args, "handler") and callable(args.handler):
        args.handler(args)
    else:
        print("[ERROR] No handler defined for this command.")


if __name__ == "__main__":
    main()
