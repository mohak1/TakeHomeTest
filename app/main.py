"""The entry point file of the app"""
import argparse

def main(**kwargs) -> None:
    raise NotImplementedError

if __name__ == '__main__':
    # pylint: disable=pointless-string-statement
    """
    Runs main() with optional arguments that can override the default
    constant values defined in config. The available args are:
        --url
        # TODO: complete this list
    """
    parser = argparse.ArgumentParser()

    # region: arguments not related to tasks
    # URL
    parser.add_argument(
        '--url',
        type=str,
        help='URL of the remote CSV file that is to be fetched'
    )
    # output directory
    parser.add_argument(
        '--output-dir',
        type=str,
        help='Full path where the output files are to be saved'
    )
    # output file names
    parser.add_argument(
        '--t1-file-name',
        type=str,
        help='Name of the file that contains result of Task 1'
    )
    parser.add_argument(
        '--t2-file-name',
        type=str,
        help='Name of the file that contains result of Task 2'
    )
    parser.add_argument(
        '--t3-file-name',
        type=str,
        help='Name of the file that contains result of Task 3'
    )
    # for running the tests
    parser.add_argument(
        '--run-tests',
        action='store_true',
        help='Runs unit tests in the tests directory'
    )
    #endregion

    # region: Task 1 constant values
    # column name
    # TODO: add validation -> should be in EXPECTED_COL_NAMES
    parser.add_argument(
        '--t1-col-name',
        type=str,
        help='Name of the column on which Task 1 is to be performed'
    )
    # endregion

    # region: Task 2 constant values
    # start date
    # TODO: add validation -> should be a valid date
    parser.add_argument(
        '--t2-start-date',
        type=str,
        help='Date from which Task 2 starts the check'
    )
    # end date
    # TODO: add validation -> should be a valid date
    parser.add_argument(
        '--t2-end-date',
        type=str,
        help='Date after which Task 2 stops the check'
    )
    # endregion

    # region: Task 3 constant values
    # column name
    # TODO: add validation -> should be in EXPECTED_COL_NAMES
    parser.add_argument(
        '--t3-col-name',
        type=str,
        help='Name of the column which is to be forecasted in Task 3'
    )
    # forecast days
    # TODO: add validation -> should be less than 31
    parser.add_argument(
        '--t3-num-days',
        type=str,
        help='Number of days to forecast of the next month'
    )
    # endregion

    args = parser.parse_args()
    # validate the args
    # prepare value dict and pass it to main()
    main()
