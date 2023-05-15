"""This file contains unit tests for functions in `tasks.py`"""

import datetime
import unittest

import pandas as pd
import tasks

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

class TestTasks(unittest.TestCase):
    def test_perform_task_1(self):
        input_data = pd.DataFrame(
            columns=['Date','Time','Outside Temperature','Hi Temperature','Low Temperature'],
            data=[
                ['31/05/2006',datetime.time(9,00),9.3,9.7,9.1],
                ['31/05/2006',datetime.time(9,10),10.1,10.4,9.7],
                ['01/06/2006',datetime.time(9,20),10.7,11.0,10.4],
                ['01/06/2006',datetime.time(9,30),11.2,11.3,10.9],
                ['02/06/2006',datetime.time(9,40),11.4,11.6,11.3],
                ['02/06/2006',datetime.time(10,10),18.6,18.6,18.5],
                ['03/06/2006',datetime.time(10,20),18.4,18.5,18.3],
                ['03/06/2006',datetime.time(10,30),18.3,18.3,18.2],
                ['04/06/2006',datetime.time(10,40),18.2,18.3,18.2],
                ['04/06/2006',datetime.time(10,50),18.4,18.6,18.3]
            ]
        )
        output = {}
        expected = {
            '31/05/2006': {'time': datetime.time(9, 10), 'temp': 10.1},
            '01/06/2006': {'time': datetime.time(9, 30), 'temp': 11.2},
            '02/06/2006': {'time': datetime.time(10, 10), 'temp': 18.6},
            '03/06/2006': {'time': datetime.time(10, 20), 'temp': 18.4},
            '04/06/2006': {'time': datetime.time(10, 50), 'temp': 18.4}
        }
        tasks.perform_task_1(input_data, 'Outside Temperature', output)
        self.assertEqual(output, expected)

    def test_perform_task_2(self):
        self.assertEqual(True, True)

    def test_perform_task_3(self):
        self.assertEqual(True, True)

    def test_get_avg_time(self):
        time1 = datetime.time(10,20)
        time2 = datetime.time(12,50)
        expected = datetime.time(11, 35)
        output = tasks.get_avg_time(time1, time2)
        self.assertEqual(output, expected)

    def test_avg_time_of_hottest_daily_temp(self):
        input_data = {
            '31/05/2006': {'time': datetime.time(14, 40), 'temp': 15.5},
            '01/06/2006': {'time': datetime.time(15, 0), 'temp': 17.2},
            '02/06/2006': {'time': datetime.time(13, 20), 'temp': 17.7},
            '03/06/2006': {'time': datetime.time(14, 50), 'temp': 19.6},
        }
        expected = [('05/2006', '14:40'), ('06/2006', '14:30')]
        output = tasks.avg_time_of_hottest_daily_temp(input_data)
        self.assertEqual(output, expected)

    def test_hottest_time_with_hightest_freq(self):
        input_data = {
            '31/05/2006': {'time': datetime.time(14, 40), 'temp': 15.5},
            '01/06/2006': {'time': datetime.time(15, 0), 'temp': 17.2},
            '02/06/2006': {'time': datetime.time(13, 20), 'temp': 17.7},
            '03/06/2006': {'time': datetime.time(14, 50), 'temp': 19.6},
        }
        expected = '14:40'
        output = tasks.hottest_time_with_hightest_freq(input_data)
        self.assertEqual(output, expected)

    def test_top_hottest_times(self):
        input_data = {
            '31/05/2006': {'time': datetime.time(14, 40), 'temp': 15.5},
            '01/06/2006': {'time': datetime.time(15, 0), 'temp': 17.2},
            '02/06/2006': {'time': datetime.time(13, 20), 'temp': 17.7},
            '03/06/2006': {'time': datetime.time(14, 50), 'temp': 19.6},
        }
        expected = [('19.6', '03/06/2006'), ('17.7', '02/06/2006'),
                ('17.2', '01/06/2006'), ('15.5', '31/05/2006')]
        output = tasks.top_hottest_times(
            input_data, 10
        )
        self.assertEqual(output, expected)
