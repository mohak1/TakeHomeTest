"""Contains functions for performing file read/write operations"""

import typing as ty

import custom_exceptions as ce


def get_full_path(dir_path: str, file_name: str):
    """
    Creates full path from directory path and file name

    Args:
        dir_path (str): full path of the directory on disk
        file_name (str): name of the file
    
    Returns:
        full_path (str): joined path by joining dir and file name
    """
    # handle trailing slash in `dir_path` string
    if dir_path[-1] == '/':
        full_path = f'{dir_path}{file_name}'
    else:
        full_path = f'{dir_path}/{file_name}'
    return full_path

def save_task_1_to_disk(
    task_1_a_result: ty.List[ty.Tuple],
    task_1_b_result: str,
    task_1_c_result: ty.List[ty.Tuple],
    top_count_value: str,
    dir_path: str,
    file_name: str,
) -> None:
    """
    Opens `file_name` at `dir_path` with append mode (`a`) and appends
    to the contents of the file. Creates a new file if the file name
    doesn't exist on the path.

    Writes the results for part a, b and c of task 1 to the file.

    Args:
        task_1_a_result: contains result for 1 a
        task_1_b_result: contains result for 1 b
        task_1_c_result: contains result for 1 c
        top_count_value: the number of top entires in result 1 c
        dir_path (str): path of the dir where file is to be saved
        file_name (str): name of the file to be saved

    Raises `FileWriteError` if an error is encountered while writing
    the output to the file
    """

    task_1_a_heading = 'Average time of hottest daily temperature (over month)'
    task_1_b_heading = 'Most commonly occurring hottest time of day'
    task_1_c_heading = f'Top {top_count_value} hottest times on distinct days'

    file_path = get_full_path(dir_path, file_name)

    try:
        with open(file=file_path, mode='a', encoding='utf-8') as file:
            # heading for 1 a
            file.write(task_1_a_heading + '\n')
            # output of 1 a
            for ele in task_1_a_result:
                file.write(ele[0] + ' ' + ele[1] + '\n')

            # heading for 1 b
            file.write('\n' + task_1_b_heading + '\n')
            # output of 1 b
            file.write(task_1_b_result + '\n')

            # heading for 1 c
            file.write('\n' + task_1_c_heading + '\n')
            # output of 1 c
            for ele in task_1_c_result:
                file.write(ele[0] + ' ' + ele[1] + '\n')
    except OSError as err:
        raise ce.FileWriteError(
            f'Error occurred while writing to file `{file_path}`\n'
            f'Traceback\n{err}'
        )

def save_task_2_to_disk(
        task_2_result: ty.List[ty.Tuple],
        dir_path: str,
        file_name: str,
) -> None:
    """
    Opens `file_name` at `dir_path` with append mode (`a`) and appends
    to the contents of the file. Creates a new file if the file name
    doesn't exist on the path.

    Writes the results of task 2 to the file.

    Args:
        task_2_result: List containing Date and Time for Task 2
        dir_path (str): path of the dir where file is to be saved
        file_name (str): name of the file to be saved

        '14:50',
        [('23.2', '06/06/2006'), ('22.4', '11/06/2006'),]

    Raises `FileWriteError` if an error is encountered while writing
    the output to the file
    """

    file_path = get_full_path(dir_path, file_name)

    try:
        with open(file=file_path, mode='a', encoding='utf-8') as file:
            # output of task 2
            for ele in task_2_result:
                file.write(ele[0] + ' ' + ele[1] + '\n')

    except OSError as err:
        raise ce.FileWriteError(
            f'Error occurred while writing to file `{file_path}`\n'
            f'Traceback\n{err}'
        )

def save_task_3_to_disk(
        task_3_result: ty.List[ty.Tuple],
        dir_path: str,
        file_name: str,
) -> None:
    """
    Opens `file_name` at `dir_path` with write mode (`w`) and replaces
    the contents of the file. Creates a new file if the file name
    doesn't exist on the path.

    Writes the results of task 3 to the file.

    Args:
        task_3_result: List containing Date, Time, Forecast for Task 3
        dir_path (str): path of the dir where file is to be saved
        file_name (str): name of the file to be saved

    Raises `FileWriteError` if an error is encountered while writing
    the output to the file
    """

    file_path = get_full_path(dir_path, file_name)

    try:
        with open(file=file_path, mode='a', encoding='utf-8') as file:
            # output of task 3
            for ele in task_3_result:
                file.write(ele[0] + ' ' + ele[1] + ' ' + ele[2] + '\n')

    except OSError as err:
        raise ce.FileWriteError(
            f'Error occurred while writing to file `{file_path}`\n'
            f'Traceback\n{err}'
        )
