"""
Contains functions that are used for performing operations on data
including cleaning, formatting, etc
"""
import logging
import sys
import typing as ty

import pandas as pd

from app import config
from app import custom_exceptions as ce
from app import tasks, validator


def transform_data(data: pd.DataFrame) -> ty.Dict:
    """
    Converts 'Date' and 'Time' column to datetime while keeping the
    original format.
    Converts the column names in config.NUMERIC_COL_NAMES to numeric

    Raises `UnSupporterdDataTypeError` if operations are performed on
    Pandas DataFrame that are not possible due to unsupported column
    values, eg: converting a date string to a number

    Args:
        data (DataFrame): the DataFrame to be cleaned and transformed

    Returns:
        (dict): the cleaned and transformed DataFrame as a dictionary
    """

    remove_cols_that_are_not_needed(data)
    convert_time_col_to_datetime(data)
    convert_column_data_to_numeric(data)
    remove_rows_where_data_is_na(data)
    return data.to_dict()

def convert_date_col_to_datetime(data: pd.DataFrame) -> None:
    """
    Converts the values in 'Date' column in the dataframe to a datetime
    object and keeps the original date formatting (DD/MM/YYYY)
    """

    try:
        data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
        data['Date'] = data['Date'].dt.strftime('%d/%m/%Y')
    except ValueError as err:
        raise ce.UnSupporterdDataTypeError(
            'An unsupported value encountered in column `Date` that '
            'cannot be converted to type `datetime`\n'
            f'Traceback:\n{err}'
        )

def convert_time_col_to_datetime(data: pd.DataFrame, format_='%H:%M') -> None:
    """
    Converts the values in 'Time' column in the dataframe to a datetime
    object for easy reference of time
    """

    try:
        data['Time'] = pd.to_datetime(data['Time'], format=format_).dt.time
    except ValueError as err:
        raise ce.UnSupporterdDataTypeError(
            'An unsupported value encountered in column `Time` that '
            'cannot be converted to type `datetime.time`\n'
            f'Traceback:\n{err}'
        )

def convert_column_data_to_numeric(data) -> None:
    """Converts the values in `col_name` to numeric type"""
    for name in config.NUMERIC_COL_NAMES:
        try:
            data[name] = pd.to_numeric(data[name])
        except ValueError as err:
            raise ce.UnSupporterdDataTypeError(
            f'An unsupported value encountered in column `{name}` that '
            'cannot be converted to a numeric type`\n'
            f'Traceback:\n{err}'
        )

def remove_cols_that_are_not_needed(data: pd.DataFrame) -> None:
    """
    Removes columns from the dataframe that are not used in any of the
    operations.
    """

    for col_name in data.columns.values:
        if col_name not in config.EXPECTED_COL_NAMES:
            data.drop(col_name, axis=1, inplace=True)

def remove_rows_where_data_is_na(data: pd.DataFrame):
    """Removes rows where value for any column is 'na'"""
    data = data.dropna(inplace=True)

def formatted_task_1_results(
    result: ty.Dict, count: int
) -> ty.Tuple[ty.List[ty.Tuple], str, ty.List[ty.Tuple]]:
    """
    Takes a dictionary as an argument and expects it to have the format
    of Task 1 output

    This is the expected format:
    {
        '01/06/2006': {'temp': 17.2, 'time': datetime.time(15, 0)},
        '01/07/2006': {'temp': 16.0, 'time': datetime.time(8, 50)},
    }

    Returns:
        A tuple contining 3 elements. Each element is a formatted output
        for task 1
        month_avg_hottest_time (list): contains tuples of date and time str
        most_common_hottest_time (str): value of most common hottest time
        top_hottest_times (list): contains tuples of temp and date str
    >>> Example:
    (
        [('05/2006', '14:40'), ('06/2006', '12:33')],
        '14:50',
        [('23.2', '06/06/2006'), ('22.4', '11/06/2006'),]
    )
    """

    try:
        validator.check_task_1_dict_format(result)
    except ce.InvalidFormatError as err:
        logging.error('Input not in valid format\n%s', str(err), exc_info=True)
        sys.exit(1)

    month_avg_hottest_time = tasks.avg_time_of_hottest_daily_temp(result)
    most_common_hottest_time = tasks.hottest_time_with_hightest_freq(result)
    top_hottest_times = tasks.top_hottest_times(result, count)

    return month_avg_hottest_time, most_common_hottest_time, top_hottest_times
