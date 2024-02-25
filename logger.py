import logging
import sys

# Create a custom formatter with ISO 8601 datetime format
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z"
)

# Create a handler that will print logs to the console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# Create a logger and set the log level
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Add the console handler to the logger
logger.addHandler(console_handler)
