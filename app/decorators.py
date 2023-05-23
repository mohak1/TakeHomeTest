"""This file contains decorators for logging and exception handling"""

import functools
import logging
import sys

import requests

from app import config
from app import custom_exceptions as ce

if config.LOGGING_LEVEL.upper() == 'INFO':
    LEVEL = logging.INFO
elif config.LOGGING_LEVEL.upper() == 'DEBUG':
    LEVEL = logging.INFO
else:
    LEVEL = logging.NOTSET

logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=LEVEL
)

def log_method(func):
    """
    This decorator logs the entry and exit of a method on INFO level
    Also logs the arguments and result values on DEBUG level

    Args:
        func: The function or method to be decorated.

    Returns:
        The decorated function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        method_name = func.__name__
        logger = logging.getLogger(__name__)
        logger.info('Entering function: `%s`', method_name)
        logger.debug('with args: %s, kwargs: %s', args, kwargs)
        result = func(*args, **kwargs)
        logger.info('`%s` executed.', method_name)
        logger.debug('result: %s', result)
        return result
    return wrapper

def exception_handler(func):
    """
    This decorator catches exceptions and exits the program

    Args:
        func: The function or method to be decorated.

    Returns:
        The decorated function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except (
            ce.DataLoadingError, ce.DataValidationError,
            ce.InvalidFormatError, ce.UnSupporterdDataTypeError,
            NotADirectoryError, OSError,
            requests.exceptions.RequestException
        ):
            # logging not needed; errors are logged when raised
            sys.exit(1)
    return wrapper
