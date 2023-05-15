"""The entry point file of the script"""
import argparse
import unittest

import config
import data_fetcher as data_f
import data_operations as data_op
import file_operations as file_op
import tasks


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
    # output dictionaries for tracking the output of tasks
    task_1_output = {}

    for data_chunk in data_f.get_data_chunk(config.URL):
        data_op.transform_data(data_chunk) # TODO: Raise/suppress exceptions
        tasks.perform_task_1(data_chunk, config.T1_COL_NAME, task_1_output)

    task_1_a, task_1_b, task_1_c = data_op.formatted_task_1_results(
        task_1_output, config.T1_COUNT_OF_TOP_HOTTEST_DAYS
    ) # TODO: Raise/suppress exceptions

    # save to file
    file_op.save_task_1_to_disk( # TODO: handle exception
        task_1_a, task_1_b, task_1_c,
        config.T1_COUNT_OF_TOP_HOTTEST_DAYS,
        config.OUTPUT_DIR, config.T1_FILE_NAME
    )

if __name__ == '__main__':
    # pylint: disable=pointless-string-statement
    """
    Runs main() with optional arguments that can override the default
    constant values defined in config. The available args are:
        --url
        # TODO: complete this list
    """
    parser = argparse.ArgumentParser()

    # region: arguments not related to tasks
    # URL
    parser.add_argument(
        '--url',
        type=str,
        help='URL of the remote CSV file that is to be fetched'
    )
    # output directory
    parser.add_argument(
        '--output_dir',
        type=str,
        help='Full path where the output files are to be saved'
    )
    # output file names
    parser.add_argument(
        '--t1_file_name',
        type=str,
        help='Name of the file that contains result of Task 1'
    )
    parser.add_argument(
        '--t2_file_name',
        type=str,
        help='Name of the file that contains result of Task 2'
    )
    parser.add_argument(
        '--t3_file_name',
        type=str,
        help='Name of the file that contains result of Task 3'
    )
    # for running the tests
    parser.add_argument(
        '--run_tests',
        action='store_true',
        help='Runs unit tests in the tests directory'
    )
    #endregion

    # region: Task 1 constant values
    # column name
    # TODO: add validation -> should be in EXPECTED_COL_NAMES
    parser.add_argument(
        '--t1_col_name',
        type=str,
        help='Name of the column on which Task 1 is to be performed'
    )
    # endregion

    # region: Task 2 constant values
    # start date
    # TODO: add validation -> should be a valid date
    parser.add_argument(
        '--t2_start_date',
        type=str,
        help='Date from which Task 2 starts the check'
    )
    # end date
    # TODO: add validation -> should be a valid date
    parser.add_argument(
        '--t2_end_date',
        type=str,
        help='Date after which Task 2 stops the check'
    )
    # endregion

    # region: Task 3 constant values
    # column name
    # TODO: add validation -> should be in EXPECTED_COL_NAMES
    parser.add_argument(
        '--t3_col_name',
        type=str,
        help='Name of the column which is to be forecasted in Task 3'
    )
    # forecast days
    # TODO: add validation -> should be less than 31
    parser.add_argument(
        '--t3_num_days',
        type=str,
        help='Number of days to forecast of the next month'
    )
    # endregion

    args = parser.parse_args()

    if args.run_tests:
        loader = unittest.TestLoader()
        suite = loader.discover(start_dir='app/tests')
        runner = unittest.TextTestRunner()
        runner.run(suite)
    else:
        # TODO: add validators for command line args
        # prepare value dict and pass it to main()
        main()
