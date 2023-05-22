"""This file contains unit tests for functions in `file_operations.py`"""
import os
import sys
import unittest
from unittest.mock import patch

sys.path.append('.')

# pylint: disable=wrong-import-position

from app import config
from app import file_operations as file_op

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

class TestValidator(unittest.TestCase):

    def setUp(self):
        test_dir = './app/tests/test_output'
        file_1 = config.T1_FILE_NAME + '-ckpt-1'
        file_2 = config.T2_FILE_NAME + '-ckpt-1'
        file_3 = config.T3_FILE_NAME + '-ckpt-1'
        t1_data = {
            '01/06/2006': {'temp': 17.2, 'time': '15:00:00'},
            '01/07/2006': {'temp': 16.0, 'time': '08:50:00'},
        }
        t2_data = [
            ('01/06/2006', '15:00'),
            ('01/07/2006', '08:50'),
        ]
        t3_data = [
            ('01/06/2006', '15:00', 10.2),
            ('01/07/2006', '08:50', 15.8),
        ]
        file_op.save_as_pkl(t1_data, file_1, test_dir)
        file_op.save_as_pkl(t2_data, file_2, test_dir)
        file_op.save_as_pkl(t3_data, file_3, test_dir)

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

    @patch('app.config.OUTPUT_DIR', './app/tests/test_output')
    def test_save_checkpoints_no_error_raised(self):
        t1_res = {
            '01/06/2006': {'temp': 17.2, 'time': '15:00:00'},
            '01/07/2006': {'temp': 16.0, 'time': '08:50:00'},
        }
        t2_res = [
            ('01/06/2006', '15:00'),
            ('01/07/2006', '08:50'),
        ]
        t3_res = [
            ('01/06/2006', '15:00', 10.2),
            ('01/07/2006', '08:50', 15.8),
        ]
        ckpt_num = 1
        file_op.save_checkpoints(t1_res, t2_res, t3_res, ckpt_num)
        test_dir_path = './app/tests/test_output'
        t1_file_name = f'{config.T1_FILE_NAME}-ckpt-{ckpt_num}.pkl'
        t2_file_name = f'{config.T2_FILE_NAME}-ckpt-{ckpt_num}.pkl'
        t3_file_name = f'{config.T3_FILE_NAME}-ckpt-{ckpt_num}.pkl'
        t1_ckpt_exists = os.path.exists(test_dir_path+'/'+t1_file_name)
        t2_ckpt_exists = os.path.exists(test_dir_path+'/'+t2_file_name)
        t3_ckpt_exists = os.path.exists(test_dir_path+'/'+t3_file_name)
        self.assertTrue(t1_ckpt_exists, True)
        self.assertTrue(t2_ckpt_exists, True)
        self.assertTrue(t3_ckpt_exists, True)

    def test_save_as_pkl_no_error_raised(self):
        test_dir = './app/tests/test_output'
        file_1 = config.T1_FILE_NAME + '-ckpt-1000'
        file_2 = config.T2_FILE_NAME + '-ckpt-1000'
        file_3 = config.T3_FILE_NAME + '-ckpt-1000'
        t1_data = {
            '01/06/2006': {'temp': 17.2, 'time': '15:00:00'},
            '01/07/2006': {'temp': 16.0, 'time': '08:50:00'},
        }
        t2_data = [
            ('01/06/2006', '15:00'),
            ('01/07/2006', '08:50'),
        ]
        t3_data = [
            ('01/06/2006', '15:00', 10.2),
            ('01/07/2006', '08:50', 15.8),
        ]
        file_op.save_as_pkl(t1_data, file_1, test_dir)
        file_op.save_as_pkl(t2_data, file_2, test_dir)
        file_op.save_as_pkl(t3_data, file_3, test_dir)
        self.assertEqual(os.path.exists(test_dir+'/'+file_1+'.pkl'), True)
        self.assertEqual(os.path.exists(test_dir+'/'+file_2+'.pkl'), True)
        self.assertEqual(os.path.exists(test_dir+'/'+file_3+'.pkl'), True)

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

    @patch('app.config.OUTPUT_DIR', './app/tests/test_output')
    def test_get_task_checkpoint_file_names(self):
        # pylint: disable=invalid-name
        t1, t2, t3 = file_op.get_task_checkpoint_file_names()
        # all t1 files should have config.T1_FILE_NAME name
        for name in t1:
            if config.T1_FILE_NAME not in name:
                self.assertEqual(True, False)
        for name in t2:
            if config.T2_FILE_NAME not in name:
                self.assertEqual(True, False)
        for name in t3:
            if config.T3_FILE_NAME not in name:
                self.assertEqual(True, False)
        self.assertEqual(True, True)

    @patch('app.config.OUTPUT_DIR', './app/tests/test_output')
    def test_gather_task_1_results(self):
        t1_file_name = config.T1_FILE_NAME+'-ckpt-1.pkl'
        output = file_op.gather_task_1_results([t1_file_name])
        self.assertEqual(isinstance(output, dict), True)

    @patch('app.config.OUTPUT_DIR', './app/tests/test_output')
    def test_gather_and_save_task_results_task2(self):
        t2_file_name = config.T1_FILE_NAME+'-ckpt-1.pkl'
        file_op.gather_and_save_task_results([t2_file_name], 2)
        dir_path = './app/tests/test_output'
        self.assertTrue(os.path.exists(dir_path+'/'+t2_file_name))

    @patch('app.config.OUTPUT_DIR', './app/tests/test_output')
    def test_gather_and_save_task_results_task3(self):
        t3_file_name = config.T1_FILE_NAME+'-ckpt-1.pkl'
        file_op.gather_and_save_task_results([t3_file_name], 3)
        dir_path = './app/tests/test_output'
        self.assertTrue(os.path.exists(dir_path+'/'+t3_file_name))

    def test_format_task_result_as_lines_task_2(self):
        t2_res = [
            ('01/06/2006', '15:00'),
            ('01/07/2006', '08:50'),
        ]
        expected = ['01/06/2006 15:00','01/07/2006 08:50']
        output = file_op.format_task_result_as_lines(t2_res, 2)
        self.assertEqual(output, expected)

    def test_format_task_result_as_lines_task_3(self):
        t3_res = [
            ('01/06/2006', '15:00', 10.2),
            ('01/07/2006', '08:50', 15.8),
        ]
        expected = ['01/06/2006 15:00 10.2', '01/07/2006 08:50 15.8']
        output = file_op.format_task_result_as_lines(t3_res, 3)
        self.assertEqual(output, expected)

    @patch('app.config.OUTPUT_DIR', './app/tests/test_output')
    def test_compile_checkpoints_to_generate_output(self):
        file_op.compile_checkpoints_to_generate_output()
        dir_path = './app/tests/test_output'
        t1_file_name = config.T1_FILE_NAME + config.FILE_EXTENSION
        t2_file_name = config.T1_FILE_NAME + config.FILE_EXTENSION
        t3_file_name = config.T1_FILE_NAME + config.FILE_EXTENSION
        self.assertTrue(os.path.exists(dir_path+'/'+t1_file_name))
        self.assertTrue(os.path.exists(dir_path+'/'+t2_file_name))
        self.assertTrue(os.path.exists(dir_path+'/'+t3_file_name))
