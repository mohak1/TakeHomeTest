"""
Contains functions that perform validation on data, argument values, etc
"""
import datetime
import os
import numbers
import typing as ty

import config
import custom_exceptions as ce


def check_task_1_dict_format(task_1_output: ty.Dict) -> None:
    """
    Task 1 output is a dictionary of dictionaries where each element of
    the dictionary is of the format:
        {
            '01/06/2006': {'temp': 17.2, 'time': datetime.time(15, 0)},
            '01/07/2006': {'temp': 16.0, 'time': datetime.time(8, 50)},
        }

    Raises `InvalidFormatError` exception if the input dictionary is
    not in the expected format
    """

    if not isinstance(task_1_output, dict):
        raise ce.InvalidFormatError(
                'Expected Task 1 output to be of type `dict` but it '
                f'is of type `{type(task_1_output)}` instead'
            )

    for key in task_1_output:
        if not isinstance(key, str):
            raise ce.InvalidFormatError(
                'Expected the key of Task 1 output dictionaries '
                f'to be of type `str` but it is `{type(task_1_output)}`'
            )

        if not isinstance(task_1_output[key], dict):
            raise ce.InvalidFormatError(
                'Expected the elements in Task 1 output dictionary to '
                f'be of type `dict` but got `{task_1_output[key]}`'
            )

        if set(task_1_output[key].keys()) != {'temp', 'time'}:
            raise ce.InvalidFormatError(
                'Expected the dictionaries in Task 1 output to '
                'have keys `{"temp", "time"}` but got '
                f'`{set(task_1_output[key].keys())}` instead'
            )

        if not isinstance(task_1_output[key]['temp'], numbers.Number):
            raise ce.InvalidFormatError(
                'Expected the value of "temp" key in Task 1 output '
                ' dictionary elements be a number but its of type '
                f'`{task_1_output[key]["temp"]}`'
            )

        if not isinstance(task_1_output[key]['time'], datetime.time):
            raise ce.InvalidFormatError(
                'Expected the value of "time" key in Task 1 output '
                ' dictionary elements be a datetime.time object but '
                f'it is of type `{task_1_output[key]["temp"]}`'
            )

def check_for_expected_columns(column_names: ty.List) -> None:
    """
    Verifies that the column names contain all the values that are
    expected for the operations, defined in config.EXPECTED_COL_NAMES

    Args:
        column_names (list): List column names fetched from URL

    """
    column_names = set(column_names)
    for name in config.EXPECTED_COL_NAMES:
        if name not in column_names:
            raise ce.ValidationError(
                'Fetched CSV does not contain expected columns.\n'
                f'Expected columns: {config.EXPECTED_COL_NAMES}\n'
                f'Fetched columns: {column_names}'
            )

def validate_dir_path(path: str) -> None:
    """
    Checks if the path points to an actual directory on disk
    Raises `NotADirectoryError` if the path is not a directory

    Args:
        path (str): the path of the directory

    Returns:
        None
    """

    if not os.path.isdir(path):
        raise NotADirectoryError(
            f'Please ensure the path `{path}` is a valid directory.'
        )
