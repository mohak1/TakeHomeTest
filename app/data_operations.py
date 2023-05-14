"""
Contains functions that are used for performing operations on data
including cleaning, formatting, etc
"""
import typing as ty

import config
import pandas as pd
import validator


def transform_data(data: pd.DataFrame) -> None:
    """
    Converts 'Date' and 'Time' column to datetime while keeping the
    original format.
    Converts the column names in config.NUMERIC_COL_NAMES to numeric
    """
    remove_cols_that_are_not_needed(data)
    convert_date_col_to_datetime(data)
    convert_time_col_to_datetime(data)
    convert_column_data_to_numeric(data)
    remove_rows_where_data_is_na(data)

def convert_date_col_to_datetime(data: pd.DataFrame) -> None:
    """
    Converts the values in 'Date' column in the dataframe to a datetime
    object and keeps the original date formatting (DD/MM/YYYY)
    """
    data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
    data['Date'] = data['Date'].dt.strftime('%d/%m/%Y')

def convert_time_col_to_datetime(data: pd.DataFrame) -> None:
    """
    Converts the values in 'Time' column in the dataframe to a datetime
    object for easy reference of time
    """
    data['Time'] = pd.to_datetime(data['Time'], format='%H:%M').dt.time

def convert_column_data_to_numeric(data) -> None:
    """Converts the values in `col_name` to numeric type"""
    for name in config.NUMERIC_COL_NAMES:
        data[name] = pd.to_numeric(data[name])

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
