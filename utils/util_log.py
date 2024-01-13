# util_log.py

import logging
import pathlib
import sys

def get_log_file() -> str:
    """
    Return the path to the log file in my parent directory.
    """
    return pathlib.Path.cwd().joinpath("logs").joinpath("log.txt")

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler and set level to info
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Create file handler which logs even debug messages
# 'w' mode in FileHandler starts a new log file each run
file_handler = logging.FileHandler(get_log_file(), mode='w')
file_handler.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s.%(levelname)s:\t%(message)s')

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
