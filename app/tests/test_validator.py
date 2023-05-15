"""This file contains unit tests for functions in `validator.py`"""

import datetime
import unittest

import config
import custom_exceptions as ce
import validator

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

class TestValidator(unittest.TestCase):

    def test_check_task_1_dict_format(self):
        valid_inp = {
            '01/06/2006': {'temp': 17.2, 'time': datetime.time(15, 0)},
            '01/07/2006': {'temp': 16.0, 'time': datetime.time(8, 50)},
        }
        invalid_inp_1 = []
        invalid_inp_2 = {1: {'temp': 17.2, 'time': datetime.time(15, 0)}}
        invalid_inp_3 = {'01/06/2006': [1,2,3]}
        invalid_inp_4 = {'01/06/2006': {'a': 17.2, 'b': datetime.time(15, 0)}}
        invalid_inp_5 = {1: {'temp': 'abc', 'time': datetime.time(15, 0)}}
        invalid_inp_6 = {1: {'temp': 17.2, 'time': '15:00'}}

        test_cases = [
            # case: input has expected format
            (valid_inp, None),

            # case: invalid format: not instance of dict
            (invalid_inp_1, ce.InvalidFormatError),

            # case: invalid format: key not str
            (invalid_inp_2, ce.InvalidFormatError),

            # case: invalid format: dict value not dict
            (invalid_inp_3, ce.InvalidFormatError),

            # case: invalid format: dict keys not 'temp' and 'time'
            (invalid_inp_4, ce.InvalidFormatError),

            # case: invalid format: value of key 'temp' is not a number
            (invalid_inp_5, ce.InvalidFormatError),

            # case: invalid format: value of key 'time' is not datetime obj
            (invalid_inp_6, ce.InvalidFormatError),

        ]
        for cols, expected in test_cases:
            with self.subTest(cols=cols, expected=expected):
                if expected is None:
                    validator.check_task_1_dict_format(cols)
                else:
                    with self.assertRaises(expected):
                        validator.check_task_1_dict_format(cols)
        self.assertEqual(True, True)

    def test_check_for_expected_columns(self):
        expected_cols = config.EXPECTED_COL_NAMES
        extra_cols = expected_cols + ['c1','c2','c3']
        test_cases = [
            # case: input has all expected columns and more
            (expected_cols, None),

            # case: input has a subset of expected columns
            (extra_cols, None),

            # case: input does not have all expected columns
            (expected_cols[:-2], ce.DataValidationError),
        ]
        for cols, expected in test_cases:
            with self.subTest(cols=cols, expected=expected):
                if expected is None:
                    validator.check_for_expected_columns(cols)
                else:
                    with self.assertRaises(expected):
                        validator.check_for_expected_columns(cols)

    def test_validate_dir_path(self):
        test_cases = [
            # case: dir exists
            ('./output', None),

            # case: dir does not exist
            ('not_a_valid_dir', NotADirectoryError),
        ]
        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                if expected is None:
                    validator.validate_dir_path(path)
                else:
                    with self.assertRaises(expected):
                        validator.validate_dir_path(path)
