"""
This file contains functions that perform operations to fetch data from
the internet
"""
import csv
import logging
import typing as ty
from collections import deque

import config
import pandas as pd
import requests

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

    Returns an empty Pandas DataFrame object if an error occurs in
    fetching the data from the passed URL

    Args:
        url (str): The URL to retrieve the data from

    Yields:
        pd.DataFrame: A Pandas DataFrame containing the data chunk
    """
    try:
        data_stream = get_data_stream(url)
    except requests.exceptions.RequestException as err:
        # TODO: mention the supressed requests error in logs
        logger.error("Error occurred during data download: %s", str(err))
        return pd.DataFrame()

    reader = csv.reader(data_stream.iter_lines(
        chunk_size=config.CHUNK_SIZE, decode_unicode=True)
    )
    rows = deque([]) # popleft() is O(1) in deque; in list pop(0) is O(N)
    col_names = []
    for row in reader:
        rows.append(row)
        if len(rows) == config.CHUNK_SIZE:
            if not col_names:
                # first row of the CSV contains the column names
                # removing first row so it doesnt get added as data row
                col_names = rows[0]
                rows.popleft()
            dframe = pd.DataFrame(columns=col_names, data=rows)
            rows = []
            yield dframe
    if rows:
        dframe = pd.DataFrame(columns=col_names, data=rows)
        yield dframe
