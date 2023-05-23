"""The entry point file of the script"""

import argparse
import sys
import unittest

sys.path.append('.') # to make 'app' folder visible from the base dir

# pylint: disable=wrong-import-position
from app import config
from app import data_fetcher as data_f
from app import data_operations as data_op
from app import decorators
from app import file_operations as file_op
from app import tasks, validator


@decorators.exception_handler
@decorators.log_method
def main() -> None:
    """
    The entry point function of the script.
    Loops over the iterator function `get_data_chunk()` to get the
    remote resource data one chunk at a time (as a pandas DataFrame).

    Data transformation operations are performed on the data chunk like
    standardising the values in the dataframe, removing rows with
    partial/incomplete data, dropping columns that are not used in any
    of the tasks (i.e. not listed in `config.EXPECTED_COL_NAMES`)

    Each transformed data chunk is passed to the three task functions.
    These functions perform their respective analysis on the data.

    A data structure (dict for task1 and list for task2 and task3) is
    used to keep track of the output of each task on the data chunks.
    These dictionary for task1 is passed as a parameter to the
    `perform_task_1` method so that the method has access to the output
    of task1 on previous data chunks. This is vital to ensure the
    correctness of the final result of task1.

    Example:
        Task to find the highest temperature of the day
        >>> iteration `i`: data chunk can have Temperature values for
        01/06/2006 from 00:00 to 15:00 where highest temperature is 15
        -> Max temperature on 01/06/2006 in chunk = 15
        -> Task output dict: {'01/06/2006': 15}

        >>> iteration `i+1`: data chunk can have Temperature values for
        01/06/2006 from 15:10 to 19:50 where highest temperature is 23
        -> Max temperature on 01/06/2006 in chunk = 23
        -> Task output dict: {'01/06/2006': 23}

        >>> iteration `i+2`: data chunk can have Temperature values for
        01/06/2006 from 20:00 to 23:50 where highest temperature is 10
        -> Max temperature on 01/06/2006 in chunk = 10
        -> Task output dict: {'01/06/2006': 23}

    Hence the task1 function needs to have access to the result of the
    previous operations in order to ensure the correctness of the result
    until all the chunks are processed.

    For task2 and task3, a list is maintatined to store the results for
    each of these task results. The result of each data chunk is added
    to these lists.

    Finally, the resutls of the three tasks are written to the disk
    The execution of the script is terminated if an error occurs
    """

    validator.validate_dir_path(config.OUTPUT_DIR)

    # for tracking the result of tasks on data chunks
    task_1_res = {}
    task_2_res = []
    task_3_res = []

    num = 0
    for num, data_chunk in enumerate(data_f.get_data_chunk(config.URL)):
        data_chunk = data_op.transform_data(data_chunk)

        chunk_result_t1 = tasks.perform_task_1.delay(data_chunk, task_1_res)
        chunk_result_t2 = tasks.perform_task_2.delay(data_chunk)
        chunk_result_t3 = tasks.perform_task_3.delay(data_chunk)

        task_1_res = chunk_result_t1.get()
        task_2_res.extend(chunk_result_t2.get())
        task_3_res.extend(chunk_result_t3.get())

        if num > 0 and num % config.SAVE_CKPT_EVERY == 0:
            # save the results so far as checkpoints
            # for task1, retain the last key-value pair, as this can be
            # useful for the next chunk
            last_key = list(task_1_res.keys())[-1]
            last_val = task_1_res[last_key]
            file_op.save_checkpoints(task_1_res, task_2_res, task_3_res, num)
            task_1_res = {last_key: last_val}
            task_2_res = []
            task_3_res = []

    if task_1_res or task_2_res or task_3_res:
        file_op.save_checkpoints(task_1_res, task_2_res, task_3_res, num+1)
        task_1_res = task_2_res = task_3_res = None

    file_op.compile_checkpoints_to_generate_output()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # for running tests locally
    parser.add_argument(
        '--run_tests',
        action='store_true',
        help='Runs unit tests in the tests directory'
    )

    args = parser.parse_args()

    if args.run_tests:
        loader = unittest.TestLoader()
        suite = loader.discover(start_dir='app/tests')
        runner = unittest.TextTestRunner()
        runner.run(suite)
    else:
        main()
