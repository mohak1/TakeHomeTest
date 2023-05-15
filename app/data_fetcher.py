"""
This file contains functions that perform operations to fetch data from
the internet
"""
import csv
import logging
import typing as ty
from collections import deque

import config
import custom_exceptions as ce
import pandas as pd
import requests
import validator

logger = logging.getLogger(__name__)

def get_data_stream(url: str) -> ty.Iterator:
    """
    Returns a GET stream of the specified URL

    Args:
        url (str): The URL to retrieve the data stream from

    Returns:
        Iterator: An iterator yielding the data stream

    Raises:
        requests.exceptions.RequestException: If an error occurs while
        making a GET request to the specified URL
    """
    return requests.get(url, stream=True, timeout=60)

def get_data_chunk(url: str) -> pd.DataFrame:
    """
    Retrieves data chunks from the specified URL. Reads the data
    chunks from the stream and converts them to the CSV format
    Converts the CSV chunk to a Pandas DataFrame and yields it

    Raises `DataFetchError` if an error is encountered in fetching the
    data from the provided URL

    Raises `DataLoadingError` if the fetched data cannot be read as CSV
    of cannot be loaded as a Pandas DataFrame

    Args:
        url (str): The URL to retrieve the data from

    Yields:
        pd.DataFrame: A Pandas DataFrame containing the data chunk
    """
    try:
        data_stream = get_data_stream(url)
    except requests.exceptions.RequestException as err:
        raise ce.DataFetchError(
            'Encountered an issue in fetching data from the URL\n'
            f'Make sure `{url}` is a valid url and supports GET request'
            f'\nTraceback: \n {err}'
        )

    reader = csv.reader(data_stream.iter_lines(
        chunk_size=config.CHUNK_SIZE, decode_unicode=True)
    )
    rows = deque([]) # popleft() is O(1) in deque; in list pop(0) is O(N)
    col_names = []
    try:
        for row in reader:
            rows.append(row)
            if len(rows) == config.CHUNK_SIZE:
                if not col_names:
                    # first row of the CSV contains column names, not data
                    # removing first row so it doesnt get added as data row
                    col_names = rows[0]
                    validator.check_for_expected_columns(col_names)
                    rows.popleft()
                dframe = pd.DataFrame(columns=col_names, data=rows)
                rows = []
                yield dframe
        if rows: # if data is smaller than chunk size
            if not col_names:
                col_names = rows[0]
                validator.check_for_expected_columns(col_names)
                rows.popleft()
            dframe = pd.DataFrame(columns=col_names, data=rows)
            yield dframe
    except (csv.Error, ValueError) as err:
        raise ce.DataLoadingError(
            'Encountered an issue in loading the fetched data \n'
            'Make sure the data being fetched is a valid CSV and '
            'contains columns expected for computation.\n'
            f'Traceback:\n{err}'
        )
    except ce.DataValidationError as err:
        raise ce.DataValidationError(
            f'The resource at `{url}` does not contain the columns '
            f'required for tasks.\nTraceback:\n{err}'
        )