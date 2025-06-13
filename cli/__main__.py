import logging
import os

from . import parser
from . import bt_logger

logger = bt_logger.get_logger(__name__)

def main():
    bt_logger.global_log_level = logging.CRITICAL
    
    logger.debug(f"Running in {os.getcwd()}")
    
    args = parser.parse()

    if hasattr(args, "handler") and callable(args.handler):
        args.handler(args)
    else:
        print("[ERROR] No handler defined for this command.")

if __name__ == "__main__":
    main()
