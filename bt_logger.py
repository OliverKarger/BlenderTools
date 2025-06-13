import logging
import sys

def get_logger(name: str) -> logging.Logger:
    new_logger = logging.getLogger(name)

    formatter = logging.Formatter('%(levelname)s:%(name)s: %(message)s')

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    new_logger.setLevel(logging.DEBUG)
    new_logger.handlers = []
    new_logger.addHandler(handler)
    return new_logger