"""This file contains unit tests for functions in `validator.py`"""
import datetime
import sys
import unittest

sys.path.append('./app')

import custom_exceptions as ce
import data_operations as data_op
import pandas as pd
from pandas.testing import assert_frame_equal

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

class TestValidator(unittest.TestCase):

    def test_transform_data_no_error_raised(self):
        pandas_df = pd.DataFrame(
            columns=['Date', 'Time', 'Temp Humidity Index   ',
            'Outside Temperature', 'WindChill', 'Hi Temperature',
            'Low Temperature', 'Outside Humidity', 'DewPoint',
            'WindSpeed', 'Hi', 'Wind Direction', 'Rain', 'Barometer',
            'Inside  Temperature', 'Inside  Humidity', 'ArchivePeriod'],
            data=[
                ['31/05/2006','09:00','9.3','9.3','9.3','9.7','9.1','55',
                 '0.8','1','7','NNW','0','1015.4','21.7','38','10'],
                ['31/05/2006',None,'9.3','9.3','9.3','9.7','9.1','55',
                 '0.8','1','7','NNW','0','1015.4','21.7','38','10'],
                ['31/05/2006','09:00','9.3',None,'9.3','9.7','9.1','55',
                 '0.8','1','7','NNW','0','1015.4','21.7','38','10'],
            ]
        )
        expected_df = pd.DataFrame(
            columns=['Date','Time','Outside Temperature','Hi Temperature',
                     'Low Temperature'],
            data=[['31/05/2006',datetime.time(9,0),9.3,9.7,9.1],]
        )
        data_op.transform_data(pandas_df)
        assert_frame_equal(pandas_df, expected_df)

    def test_transform_data_error_raised(self):
        pandas_df = pd.DataFrame(
            columns=['Date', 'Time', 'Temp Humidity Index   ',
            'Outside Temperature', 'WindChill', 'Hi Temperature',
            'Low Temperature', 'Outside Humidity', 'DewPoint',
            'WindSpeed', 'Hi', 'Wind Direction', 'Rain', 'Barometer',
            'Inside  Temperature', 'Inside  Humidity', 'ArchivePeriod'],
            data=[
                ['31/05/2006','NotATime','9.3','9.3','9.3','9.7','9.1','55',
                 '0.8','1','7','NNW','0','1015.4','21.7','38','10'],
                ['NotADate','09:00','9.3','9.3','9.3','9.7','9.1','55',
                 '0.8','1','7','NNW','0','1015.4','21.7','38','10'],
                ['31/05/2006','09:00','9.3',None,'9.3','9.7','9.1','55',
                 '0.8','1','7','NNW','0','1015.4','21.7','38','10'],
            ]
        )
        with self.assertRaises(ce.UnSupporterdDataTypeError):
            data_op.transform_data(pandas_df)

    def test_convert_date_col_to_datetime_no_error_raised(self):
        input_with_str_vals = pd.DataFrame(
            columns=['Date','Time','Outside Temperature','Hi Temperature',
                     'Low Temperature'],
            data=[
                ['31/05/2006','09:00','9.3','9.7','9.1'],
                ['31/05/2006','09:00','9.3','9.7','9.1'],
            ]
        )
        expected_df = pd.DataFrame(
            columns=['Date','Time','Outside Temperature','Hi Temperature',
                     'Low Temperature'],
            data=[
                ['31/05/2006','09:00','9.3','9.7','9.1'],
                ['31/05/2006','09:00','9.3','9.7','9.1'],
            ]
        )
        data_op.convert_date_col_to_datetime(input_with_str_vals)
        assert_frame_equal(input_with_str_vals, expected_df)

    def test_convert_date_col_to_datetime_error_raised(self):
        input_with_wrong_dates = pd.DataFrame(
            columns=['Date','Time','Outside Temperature','Hi Temperature',
                     'Low Temperature'],
            data=[
                ['31/05/2006','09:00','9.3','9.7','9.1'],
                ['NotADate','09:00','9.3','9.7','9.1'],
            ]
        )
        with self.assertRaises(ce.UnSupporterdDataTypeError):
            data_op.convert_date_col_to_datetime(input_with_wrong_dates)

    def test_convert_time_col_to_datetime_no_error_raised(self):
        input_with_str_vals = pd.DataFrame(
            columns=['Date','Time','Outside Temperature','Hi Temperature',
                     'Low Temperature'],
            data=[
                ['31/05/2006','09:00','9.3','9.7','9.1'],
                ['31/05/2006','09:00','9.3','9.7','9.1'],
            ]
        )
        expected_df = pd.DataFrame(
            columns=['Date','Time','Outside Temperature','Hi Temperature',
                     'Low Temperature'],
            data=[
                ['31/05/2006',datetime.time(9,0),'9.3','9.7','9.1'],
                ['31/05/2006',datetime.time(9,0),'9.3','9.7','9.1'],
            ]
        )
        data_op.convert_time_col_to_datetime(input_with_str_vals)
        assert_frame_equal(input_with_str_vals, expected_df)

    def test_convert_time_col_to_datetime_error_raised(self):
        input_with_wrong_time = pd.DataFrame(
            columns=['Date','Time','Outside Temperature','Hi Temperature',
                     'Low Temperature'],
            data=[
                ['31/05/2006','09:00','9.3','9.7','9.1'],
                ['31/05/2006','NotATime','9.3','9.7','9.1'],
            ]
        )
        with self.assertRaises(ce.UnSupporterdDataTypeError):
            data_op.convert_time_col_to_datetime(input_with_wrong_time)

    def test_convert_column_data_to_numeric_no_error_raised(self):
        input_with_str_vals = pd.DataFrame(
            columns=['Date','Time','Outside Temperature','Hi Temperature',
                     'Low Temperature'],
            data=[
                ['31/05/2006','09:00','9.3','9.7','9.1'],
                ['31/05/2006','09:00','9.3','9.7','9.1'],
            ]
        )
        expected_df = pd.DataFrame(
            columns=['Date','Time','Outside Temperature','Hi Temperature',
                     'Low Temperature'],
            data=[
                ['31/05/2006','09:00',9.3,9.7,9.1],
                ['31/05/2006','09:00',9.3,9.7,9.1],
            ]
        )
        data_op.convert_column_data_to_numeric(input_with_str_vals)
        assert_frame_equal(input_with_str_vals, expected_df)

    def test_convert_column_data_to_numeric_error_raised(self):
        input_with_str_vals = pd.DataFrame(
            columns=['Date','Time','Outside Temperature','Hi Temperature',
                     'Low Temperature'],
            data=[
                ['31/05/2006','09:00','9.3','9.7','9.1'],
                ['31/05/2006','09:00','a','b','c'],
            ]
        )
        with self.assertRaises(ce.UnSupporterdDataTypeError):
            data_op.convert_column_data_to_numeric(input_with_str_vals)

    def test_remove_cols_that_are_not_needed_has_unwanted_cols(self):
        input_with_unwanted_cols = pd.DataFrame(
            columns=['Date', 'Time', 'Temp Humidity Index   ',
            'Outside Temperature', 'WindChill', 'Hi Temperature',
            'Low Temperature', 'Outside Humidity', 'DewPoint',
            'WindSpeed', 'Hi', 'Wind Direction', 'Rain', 'Barometer',
            'Inside  Temperature', 'Inside  Humidity', 'ArchivePeriod'],
            data=[
                ['31/05/2006','09:00','9.3','9.3','9.3','9.7','9.1','55',
                 '0.8','1','7','NNW','0','1015.4','21.7','38','10'],
                ['31/05/2006','09:00','9.3','9.3','9.3','9.7','9.1','55',
                 '0.8','1','7','NNW','0','1015.4','21.7','38','10'],
            ]
        )
        expected_df = pd.DataFrame(
            columns=['Date','Time','Outside Temperature','Hi Temperature',
                     'Low Temperature'],
            data=[
                ['31/05/2006','09:00','9.3','9.7','9.1'],
                ['31/05/2006','09:00','9.3','9.7','9.1'],
            ]
        )

        data_op.remove_cols_that_are_not_needed(input_with_unwanted_cols)
        assert_frame_equal(input_with_unwanted_cols, expected_df)

    def test_remove_cols_that_are_not_needed_no_unwanted_cols(self):
        input_without_unwanted_cols = pd.DataFrame(
            columns=['Date','Time','Outside Temperature','Hi Temperature',
                     'Low Temperature'],
            data=[
                ['31/05/2006','09:00','9.3','9.7','9.1'],
                ['31/05/2006','09:00','9.3','9.7','9.1'],
            ]
        )
        expected_df = pd.DataFrame(
            columns=['Date','Time','Outside Temperature','Hi Temperature',
                     'Low Temperature'],
            data=[
                ['31/05/2006','09:00','9.3','9.7','9.1'],
                ['31/05/2006','09:00','9.3','9.7','9.1'],
            ]
        )

        data_op.remove_cols_that_are_not_needed(input_without_unwanted_cols)
        assert_frame_equal(input_without_unwanted_cols, expected_df)

    def test_remove_rows_where_data_is_na_with_na_data(self):
        input_with_none_vals = pd.DataFrame(
            columns=['Date', 'Time', 'Temp Humidity Index   ',
            'Outside Temperature', 'WindChill', 'Hi Temperature',
            'Low Temperature', 'Outside Humidity', 'DewPoint',
            'WindSpeed', 'Hi', 'Wind Direction', 'Rain', 'Barometer',
            'Inside  Temperature', 'Inside  Humidity', 'ArchivePeriod'],
            data=[
                ['31/05/2006','09:00','9.3','9.3','9.3','9.7','9.1','55',
                 '0.8','1','7','NNW','0','1015.4','21.7','38','10'],
                [None,'09:00','9.3','9.3','9.3','9.7','9.1','55',
                 '0.8','1','7','NNW','0',None,'21.7','38','10'],
            ]
        )
        expected_df_when_none_vals = pd.DataFrame(
            columns=['Date', 'Time', 'Temp Humidity Index   ',
            'Outside Temperature', 'WindChill', 'Hi Temperature',
            'Low Temperature', 'Outside Humidity', 'DewPoint',
            'WindSpeed', 'Hi', 'Wind Direction', 'Rain', 'Barometer',
            'Inside  Temperature', 'Inside  Humidity', 'ArchivePeriod'],
            data=[
                ['31/05/2006','09:00','9.3','9.3','9.3','9.7','9.1','55',
                 '0.8','1','7','NNW','0','1015.4','21.7','38','10'],
            ]
        )

        data_op.remove_rows_where_data_is_na(input_with_none_vals)
        assert_frame_equal(input_with_none_vals, expected_df_when_none_vals)

    def test_remove_rows_where_data_is_na_without_na_data(self):

        input_with_no_none_vals = pd.DataFrame(
            columns=['Date','Time','Outside Temperature','Hi Temperature',
                     'Low Temperature'],
            data=[
                ['31/05/2006','09:00','9.3','9.7','9.1'],
                ['31/05/2006','09:00','9.3','9.7','9.1'],
            ]
        )
        expected_df_when_no_none_vals = pd.DataFrame(
            columns=['Date','Time','Outside Temperature','Hi Temperature',
                     'Low Temperature'],
            data=[
                ['31/05/2006','09:00','9.3','9.7','9.1'],
                ['31/05/2006','09:00','9.3','9.7','9.1'],
            ]
        )
        data_op.remove_rows_where_data_is_na(input_with_no_none_vals)
        assert_frame_equal(input_with_no_none_vals, expected_df_when_no_none_vals)

    def test_formatted_task_1_results_no_error_raised(self):
        input_data = {
            '31/05/2006': {'time': datetime.time(14, 40), 'temp': 15.5},
            '01/06/2006': {'time': datetime.time(15, 0), 'temp': 17.2},
            '02/06/2006': {'time': datetime.time(13, 20), 'temp': 17.7},
            '03/06/2006': {'time': datetime.time(14, 50), 'temp': 19.6},
        }
        expected = (
            [('05/2006', '14:40'), ('06/2006', '14:30')],
            '14:40',
            [('19.6', '03/06/2006'), ('17.7', '02/06/2006'),
                ('17.2', '01/06/2006'), ('15.5', '31/05/2006')],
        )
        result = data_op.formatted_task_1_results(
            input_data, 10
        )
        self.assertEqual(result, expected)
