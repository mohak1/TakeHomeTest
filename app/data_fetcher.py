"""
This file contains functions that perform operations to fetch data from
the internet
"""
import csv
import logging
import typing as ty
from collections import deque

import pandas as pd
import requests

from app import config
from app import custom_exceptions as ce
from app import validator


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

    Args:
        url (str): The URL to retrieve the data from

    Yields:
        pd.DataFrame: A Pandas DataFrame containing the data chunk
    """
    try:
        data_stream = get_data_stream(url)
    except requests.exceptions.RequestException as err:
        logging.error('Error in fetching from URL\n%s', str(err), exc_info=True)
        return pd.DataFrame()

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
        if rows: # if data is smaller than chunk size
            if not col_names:
                col_names = rows[0]
                validator.check_for_expected_columns(col_names)
                rows.popleft()
            dframe = pd.DataFrame(columns=col_names, data=rows)
            yield dframe
    except (csv.Error, ValueError) as err:
        logging.error('Error in handling CSV\n%s', str(err), exc_info=True)
        return pd.DataFrame()

    except ce.DataValidationError as err:
        logging.error('Column mismatch in dataframe\n%s', str(err), exc_info=True)
        return pd.DataFrame()
