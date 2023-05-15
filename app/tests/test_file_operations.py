"""This file contains unit tests for functions in `file_operations.py`"""
import os
import sys
import unittest

sys.path.append('./app')

import file_operations as file_op

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

class TestValidator(unittest.TestCase):

    def test_get_full_path_no_trailing_slash(self):
        dir_path = 'a/b/c'
        file_name = 'd.txt'
        output = file_op.get_full_path(dir_path, file_name)
        expected = 'a/b/c/d.txt'
        self.assertEqual(output, expected)

    def test_get_full_path_has_trailing_slash(self):
        dir_path = 'a/b/c/'
        file_name = 'd.txt'
        output = file_op.get_full_path(dir_path, file_name)
        expected = 'a/b/c/d.txt'
        self.assertEqual(output, expected)

    def test_save_task_1_to_disk_no_error_raised(self):
        task_1_a = [('05/2006', '14:40'), ('06/2006', '12:33')]
        task_1_b = '14:50'
        task_1_c = [('23.2', '06/06/2006'), ('22.4', '11/06/2006')]
        dir_path = './app/tests/test_output'
        file_name = 't1_test.txt'
        file_op.save_task_1_to_disk(
            task_1_a, task_1_b, task_1_c,
            top_count_value=5,
            dir_path=dir_path, file_name=file_name
        )
        self.assertTrue(os.path.exists(dir_path+'/'+file_name))

    def test_save_task_2_to_disk_no_error_raised(self):
        task_2_res = [('05/2006', '14:40'), ('06/2006', '12:33')]
        dir_path = './app/tests/test_output'
        file_name = 't2_test.txt'
        file_op.save_task_2_to_disk(
            task_2_res, dir_path=dir_path, file_name=file_name
        )
        self.assertTrue(os.path.exists(dir_path+'/'+file_name))

    def test_save_task_3_to_disk_no_error_raised(self):
        task_3_res = [('05/2006', '14:40', '10.01'), ('06/2006', '12:33', '12.00')]
        dir_path = './app/tests/test_output'
        file_name = 't3_test.txt'
        file_op.save_task_3_to_disk(
            task_3_res, dir_path=dir_path, file_name=file_name
        )
        self.assertTrue(os.path.exists(dir_path+'/'+file_name))
