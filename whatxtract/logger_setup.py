import logging
from logging.handlers import RotatingFileHandler
from constants import *
from constants import __package__

try:
    from colorlog import ColoredFormatter
except ImportError:
    import sys
    import subprocess
    print('[ * ] Installing colorlog...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'colorlog'])
    from colorlog import ColoredFormatter


class StreamToLogger:
    """
    Redirects print() calls to a logger as INFO while preserving console output.
    """
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def write(self, message):
        message = message.strip()
        if message:
            self.logger.info(message)

    def flush(self):
        pass


def setup_logger(name: str = __package__) -> logging.Logger:
    """
    Sets up and returns a logger instance with console and rotating file handlers.
    Also redirects `print()` to log as INFO level.
    :rtype: logging.Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    if not logger.handlers:
        # Formatter for files
        file_formatter = logging.Formatter(LOG_FORMAT)

        # Colored formatter for console
        if ColoredFormatter:
            color_formatter = ColoredFormatter(
                "%(log_color)s%(asctime)s [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                log_colors={
                    "DEBUG":    "cyan",
                    "INFO":     "green",
                    "WARNING":  "yellow",
                    "ERROR":    "red",
                    "CRITICAL": "bold_red",
                },
            )
        else:
            color_formatter = file_formatter  # fallback

        # Console handler with colors
        stream_handler = logging.StreamHandler(sys.__stdout__)
        stream_handler.setFormatter(color_formatter)
        logger.addHandler(stream_handler)

        # Rotating file handler (5MB, 3 backups)
        rotating_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
        rotating_handler.setFormatter(file_formatter)
        logger.addHandler(rotating_handler)

    # Redirect print() output
    sys.stdout = StreamToLogger(logger)

    return logger
