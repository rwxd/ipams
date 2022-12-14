import logging
import logging.handlers
from os import getenv
from sys import stderr

LOG_LEVEL = getenv('LOG_LEVEL') or 'WARNING'

logging_format = (
    '%(levelname)s - %(asctime)s - %(name)s - '
    + '%(filename)s - %(funcName)s - %(lineno)s - %(message)s'
)

default_formatter = logging.Formatter(logging_format)

default_stream_handler = logging.StreamHandler(stderr)
default_stream_handler.setLevel(LOG_LEVEL)
default_stream_handler.setFormatter(default_formatter)

logger = logging.getLogger('ipams')
logger.addHandler(default_stream_handler)

logger.setLevel('DEBUG')
