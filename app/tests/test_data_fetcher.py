"""This file contains unit tests for functions in `data_fetcher.py`"""

import sys
import unittest
from unittest.mock import patch

sys.path.append('./app')

import data_fetcher as data_f
import pandas as pd

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

class TestGetDataStream(unittest.TestCase):

    def test_valid_url(self):
        url = 'https://www.google.com'
        response = data_f.get_data_stream(url)
        self.assertEqual(response.ok, True)


class TestDataChunk(unittest.TestCase):

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
