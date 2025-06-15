import logging
import sys

logging.basicConfig(level=logging.DEBUG)


class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[95m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"


def get_logger(name: str) -> logging.Logger:
    """
    Provides functionality to create and configure a logger with a custom format
    and stream handler. Ensures the logger avoids duplicate logging by disabling
    propagation and only adds handlers if none exist.

    Parameters:
        name (str): The name of the logger to be created or retrieved.

    Returns:
        logging.Logger: A configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.propagate = False  # Prevent log duplication via parent

    if not logger.handlers:
        formatter = ColorFormatter("[%(levelname)s] %(name)s: %(message)s")
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
