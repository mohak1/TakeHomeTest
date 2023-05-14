"""This file contains unit tests for functions in `data_fetcher.py`"""

import unittest
from unittest.mock import patch

import data_fetcher as data_f
import pandas as pd
import requests
import custom_exceptions as ce

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

class TestGetDataStream(unittest.TestCase):

    def test_valid_url(self):
        url = 'https://www.google.com'
        response = data_f.get_data_stream(url)
        self.assertEqual(response.ok, True)

    def test_url_with_invalid_format(self):
        url = 'ThisIsAnInvalidURLFormat'
        # assert if the RequestException is eaised
        with self.assertRaises(requests.exceptions.RequestException):
            data_f.get_data_stream(url)

    def test_invalid_url_with_valid_format(self):
        url = 'https://invalidURL.com'
        # assert if the RequestException is eaised
        with self.assertRaises(requests.exceptions.RequestException):
            data_f.get_data_stream(url)


class TestDataChunk(unittest.TestCase):

    def test_data_fetch_error(self):
        with self.assertRaises(ce.DataFetchError):
            list(data_f.get_data_chunk('url'))

    @patch('validator.check_for_expected_columns')
    @patch('data_fetcher.get_data_stream')
    def test_successful_data_chunk(
        self, mock_get_data_stream, mock_check_for_expected_columns
    ):
        mock_data_stream = MockValidDataStream()
        mock_get_data_stream.return_value = mock_data_stream
        mock_check_for_expected_columns.return_value = None
        expected = pd.DataFrame(
            columns=['c1', 'c2', 'c3', 'c4'],
            data=[['d1', 'd2', 'd3', 'd4'], ['d1', 'd2', 'd3', 'd4']]
        )
        result = list(data_f.get_data_chunk('url'))
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].equals(expected))

    @patch('validator.check_for_expected_columns')
    @patch('data_fetcher.get_data_stream')
    def test_value_error(
        self, mock_get_data_stream, mock_check_for_expected_columns
    ):
        mock_data_stream = MockInValidDataStream()
        mock_get_data_stream.return_value = mock_data_stream
        mock_check_for_expected_columns.return_value = None
        with self.assertRaises(ce.DataLoadingError):
            list(data_f.get_data_chunk('url'))

    @patch('validator.check_for_expected_columns')
    @patch('data_fetcher.get_data_stream')
    def test_csv_error(
        self, mock_get_data_stream, mock_check_for_expected_columns
    ):
        mock_data_stream = MockInValidCSVDataStream()
        mock_get_data_stream.return_value = mock_data_stream
        mock_check_for_expected_columns.return_value = None
        with self.assertRaises(ce.DataLoadingError):
            list(data_f.get_data_chunk('url'))

    @patch('data_fetcher.get_data_stream')
    def test_validation_error(self, mock_get_data_stream):
        mock_data_stream = MockValidDataStream()
        mock_get_data_stream.return_value = mock_data_stream
        with self.assertRaises(ce.DataValidationError):
            list(data_f.get_data_chunk('url'))

# pylint: disable=unused-argument
# pylint: disable=too-few-public-methods

class MockValidDataStream:
    def __init__(self):
        self.iter_lines = self.mock_iter_lines

    def mock_iter_lines(self, **kwargs):
        # mocked response of iter_lines()
        return [
            'c1,c2,c3,c4',
            'd1,d2,d3,d4',
            'd1,d2,d3,d4',
        ]

class MockInValidDataStream:
    def __init__(self):
        self.iter_lines = self.mock_iter_lines

    def mock_iter_lines(self, **kwargs):
        # mocked response of iter_lines()
        return [
            'c1,c2',
            'd1,d2,d3,d4',
            'd1,d2,d3,d4',
        ]

class MockInValidCSVDataStream:
    def __init__(self):
        self.iter_lines = self.mock_iter_lines

    def mock_iter_lines(self, **kwargs):
        # mocked response of iter_lines()
        return [
            ['c1,c2,c3,c4'],
            ['d1,d2,d3,d4'],
            ['d1,d2,d3,d4'],
        ]
