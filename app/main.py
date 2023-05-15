"""The entry point file of the script"""
import argparse
import logging
import unittest

import sys
import config
import data_fetcher as data_f
import data_operations as data_op
import file_operations as file_op
import custom_exceptions as ce
import tasks
import validator

logging.basicConfig(level=logging.INFO)

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
    Output dictionaries (one for each task, declared outside the loop)
    are used to keep track of the result of performing the task on each
    data chunk. These dictionaries are passed as a parameter to each
    task function so that the task functions have access to the result
    of previous operations. This is vital to ensure the correctness of
    the results partial data is passed in each chunk.

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

    Hence the task functions needs to have access to the result of the
    previous operations in order to ensure the correctness of the result
    until all the chunks are processed.

    The results are written to a file on the disk
    """
    logging.info('starting execution')
    try:
        validator.validate_dir_path(config.OUTPUT_DIR)
    except NotADirectoryError as err:
        logging.error('Invalid directory Path\n%s', str(err), exc_info=True)
        sys.exit(1)

    # output dictionaries for tracking the output of tasks
    task_1_output = {}
    task_2_output = []
    task_3_output = []

    for data_chunk in data_f.get_data_chunk(config.URL):
        try:
            data_op.transform_data(data_chunk)
        except ce.UnSupporterdDataTypeError as err:
            logging.error('Data transformation error\n%s', str(err), exc_info=True)
            sys.exit(1)

        tasks.perform_task_1(data_chunk, config.T1_COL_NAME, task_1_output)
        tasks.perform_task_2(data_chunk, task_2_output)
        tasks.perform_task_3(data_chunk, task_3_output)

    task_1_a, task_1_b, task_1_c = data_op.formatted_task_1_results(
        task_1_output, config.T1_COUNT_OF_TOP_HOTTEST_DAYS
    )

    logging.info('starting save operation')
    # save to file
    file_op.save_task_1_to_disk(
        task_1_a, task_1_b, task_1_c,
        config.T1_COUNT_OF_TOP_HOTTEST_DAYS,
        config.OUTPUT_DIR, config.T1_FILE_NAME
    )

    file_op.save_task_2_to_disk(
        task_2_output, config.OUTPUT_DIR, config.T2_FILE_NAME
    )

    file_op.save_task_3_to_disk(
        task_3_output, config.OUTPUT_DIR, config.T3_FILE_NAME
    )

    logging.info('task completed')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # for running the tests locally
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
