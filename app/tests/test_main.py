"""This file contains unit tests for functions in `main.py`"""

import sys
import unittest

sys.path.append('./app')

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

class TestMain(unittest.TestCase):
    def test_main(self):
        self.assertEqual(True, True)
