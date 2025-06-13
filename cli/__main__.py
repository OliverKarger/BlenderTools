import logging

from . import parser
from .. import bt_logger

def main():
    bt_logger.global_log_level = logging.CRITICAL
    args = parser.parse()

    if hasattr(args, "handler") and callable(args.handler):
        args.handler(args)
    else:
        print("[ERROR] No handler defined for this command.")

if __name__ == "__main__":
    main()
