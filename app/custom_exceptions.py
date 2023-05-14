"""Contains custom exceptions that are used in the script"""

# pylint: disable=unnecessary-pass

class InvalidFormatError(Exception):
    """Raised when an object is not in the expected format"""
    pass

class DataFetchError(Exception):
    """Raised when data stream cannot be fetched successfully"""
    pass

class DataLoadingError(Exception):
    """Raised data cannot be read as a CSV or Pandas DataFrame"""
    pass
