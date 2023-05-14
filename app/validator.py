"""
Contains functions that perform validation on data, argument values, etc
"""
import datetime
import numbers
import typing as ty

import config
import custom_exceptions as ce


def check_command_line_args() -> None:
    raise NotImplementedError

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
