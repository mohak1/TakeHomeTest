"""Contains custom exceptions that are used in the script"""

# pylint: disable=unnecessary-pass

class InvalidFormatError(Exception):
    """Raised when an object is not in the expected format"""
    pass

class DataFetchError(Exception):
    """Raised when data stream cannot be fetched successfully"""
    pass

class DataLoadingError(Exception):
    """Raised when data cannot be read as a CSV or Pandas DataFrame"""
    pass

class DataValidationError(Exception):
    """
    Raised when data is a valid CSV or Pandas DataFrame but does not
    contain the expected columns names or does not contain the expected
    data type in column(s)
    """
    pass

class UnSupporterdDataTypeError(Exception):
    """
    Raised when a datatype is encountered that is not supported by the
    operation.
    Example:
        When converting a Pandas DataFrame column values from string
        to number but a value is encountered that is non numeric
    """
    pass

class FileWriteError(Exception):
    """
    Raised when an error occurs while writing to a file. Likely caused
    when the file is moved/deleted during the operation
    """
    pass
