"""Contains functions for performing file read/write operations"""

import logging
import os
import pickle
import typing as ty

from app import config
from app import data_operations as data_op


def get_full_path(dir_path: str, file_name: str):
    """
    Creates full path from directory path and file name

    Args:
        dir_path (str): full path of the directory on disk
        file_name (str): name of the file
    
    Returns:
        full_path (str): joined path by joining dir and file name
    """

    if dir_path[-1] == '/':
        full_path = f'{dir_path}{file_name}'
    else:
        full_path = f'{dir_path}/{file_name}'
    return full_path

def save_checkpoints(
    t1_result: ty.Dict,
    t2_result: ty.List[ty.Tuple],
    t3_result: ty.List[ty.Tuple],
    ckpt_num: int,
) -> None:
    """
    Saves the values of task1, task2 and task3 result variables in a
    pickle file.

    Args:
        t1_result (dict): Result of task 1 until checkpoint
        t2_result (list): Result of task 2 until checkpoint
        t3_result (list): Result of task 3 until checkpoint
        ckpt_num (int): Checkpoint count

    Raises:
        - `OSError`: If an error occurs while saving the pkl files
    """

    t1_file_name = config.T1_FILE_NAME + f'-ckpt-{ckpt_num}'
    save_as_pkl(t1_result, t1_file_name, config.OUTPUT_DIR)

    t2_file_name = config.T2_FILE_NAME + f'-ckpt-{ckpt_num}'
    save_as_pkl(t2_result, t2_file_name, config.OUTPUT_DIR)

    t3_file_name = config.T3_FILE_NAME + f'-ckpt-{ckpt_num}'
    save_as_pkl(t3_result, t3_file_name, config.OUTPUT_DIR)

def save_as_pkl(
    data: ty.Union[ty.Dict, ty.List],
    file_name: str,
    dir_path: str,
) -> None:
    """
    Opens `file_name` at `dir_path` in byte-write mode (`wb`) and writes
    the contents to the file. Creates a new file if the file name
    doesn't exist on the path.

    Args:
        data (dict | list): data structure (and data) to be saved
        dir_path (str): path of the dir where file is to be saved
        file_name (str): name of the file to be saved

    Raises:
        - `OSError` if a problem occurs in reading/writing to file
    """

    file_path = get_full_path(dir_path, file_name) + '.pkl'
    try:
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)
    except OSError as err:
        logging.error('Error during saving `%s`\n%s', file_name, str(err))
        raise OSError from err

def append_lines_to_file(
    lines: ty.List, dir_path: str, file_name: str
) -> None:
    """
    Opens `file_name` at `dir_path` in append mode (`a`) and appends
    the contents to the end of file. Creates a new file if the file name
    doesn't exist on the path.

    Args:
        lines (list): List of str that are to be appended to the file
        dir_path (str): path of the dir where file is to be saved
        file_name (str): name of the file to be saved

    Raises:
        - `OSError` if a problem occurs in reading/writing to file
    """

    file_path = get_full_path(dir_path, file_name) + config.FILE_EXTENSION

    try:
        with open(file=file_path, mode='a', encoding='utf-8') as file:
            for line in lines:
                file.write(line + '\n')
    except OSError as err:
        logging.error('Error while appending to `%s`\n%s', file_name,
            str(err), exc_info=True)
        raise OSError from err

def save_task_1_to_disk(
    task_1_a_result: ty.List[ty.Tuple],
    task_1_b_result: str,
    task_1_c_result: ty.List[ty.Tuple],
    top_count_value: str,
    dir_path: str,
    file_name: str,
) -> None:
    """
    Opens `file_name` at `dir_path` with write mode (`w`) and replaces
    the contents of the file. Creates a new file if the file name
    doesn't exist on the path.

    Writes the results for part a, b and c of task 1 to the file.

    Args:
        task_1_a_result: contains result for 1 a
        task_1_b_result: contains result for 1 b
        task_1_c_result: contains result for 1 c
        top_count_value: the number of top entires in result 1 c
        dir_path (str): path of the dir where file is to be saved
        file_name (str): name of the file to be saved
    """

    task_1_a_heading = 'Average time of hottest daily temperature (over month)'
    task_1_b_heading = 'Most commonly occurring hottest time of day'
    task_1_c_heading = f'Top {top_count_value} hottest times on distinct days'

    file_path = get_full_path(dir_path, file_name)

    try:
        with open(file=file_path, mode='w', encoding='utf-8') as file:
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
        logging.error('Error during file write\n%s', str(err), exc_info=True)
        raise OSError from err

def get_task_checkpoint_file_names() -> ty.Tuple[ty.List, ty.List, ty.List]:
    """
    Returns a tuple of lists containing task checkpoint file names

    Returns:
        (`task_1_ckpts`, `task_2_ckpts`, `task_3_ckpts`):
        A tuple contining 3 elements with ckpt file names of each tsk
        - `task_1_ckpts` (list): contains pkl file names for task 1
        - `task_2_ckpts` (list): contains pkl file names for task 2
        - `task_3_ckpts` (list): contains pkl file names for task 3
    """

    # gather all the files in output dir that have .pkl extension
    pkl_files = []
    for name in os.listdir(config.OUTPUT_DIR):
        if name[-4:] == '.pkl':
            pkl_files.append(name)

    # sort them based on task number and checkpoint number
    pkl_files = sorted(pkl_files,key=lambda name: (
            name.split('-')[0], int(name.split('-')[2].split('.')[0]))
    )

    task_1_ckpts = []
    task_2_ckpts = []
    task_3_ckpts = []
    for name in pkl_files:
        if name.split('-')[0] == config.T1_FILE_NAME:
            task_1_ckpts.append(name)
        elif name.split('-')[0] == config.T2_FILE_NAME:
            task_2_ckpts.append(name)
        elif name.split('-')[0] == config.T3_FILE_NAME:
            task_3_ckpts.append(name)

    return task_1_ckpts, task_2_ckpts, task_3_ckpts

def gather_task_1_results(t1_ckpts: ty.List[str]) -> ty.Dict:
    """
    Gathers task 1 result dict from the given checkpoint file names.

    Args:
        t1_ckpts (list): A list of task 1 checkpoint file names

    Returns:
        task_1_output (dict): A dict containing the task 1 results

    Raises:
        - `OSError` if an error occurs in reading a pkl file
    """

    task_1_output = {}
    for name in t1_ckpts:
        file_path = get_full_path(config.OUTPUT_DIR, name)
        try:
            with open(file_path, 'rb') as file:
                task_1_output.update(pickle.load(file))
        except OSError as err:
            logging.error('Error when opening `%s`\n%s', name, str(err),
                exc_info=True)
            raise OSError from err

    return task_1_output

def gather_and_save_task_results(ckpts: ty.List[str], task_num: int) -> None:
    """
    Gathers and saves the results for task 2 or 3 (depeding on args)

    Args:
        ckpts (list): A list of checkpoint file names
        task_num (int): An integer representing the task number (2 or 3)

    Returns:
        None

    Raises:
        - `OSError` if an error occurs in reading or writing file
    """

    for name in ckpts:
        file_path = get_full_path(config.OUTPUT_DIR, name)
        task_output = []
        try:
            with open(file_path, 'rb') as file:
                task_output = pickle.load(file)
        except OSError as err:
            logging.error('Error when opening `%s`\n%s', name, str(err), exc_info=True)
            raise OSError from err

        lines = format_task_result_as_lines(task_output, task_num)
        file_name = name.split('-ckpt-')[0]
        append_lines_to_file(lines, config.OUTPUT_DIR, file_name)

def format_task_result_as_lines(
        task_result: ty.List[ty.Tuple], task_num: int
) -> ty.List[str]:
    """
    Formats the task output as list of strings based on the task number.

    Args:
        output (list): The task output to be formatted
        task_num (int): An integer representing the task number

    Returns:
        lines (list): A list of formatted task output lines
    """

    lines = []
    for ele in task_result:
        if task_num == 2:
            line = f'{ele[0]} {ele[1]}'
        elif task_num == 3:
            line = f'{ele[0]} {ele[1]} {ele[2]}'
        lines.append(line)
    return lines

def compile_checkpoints_to_generate_output() -> None:
    """
    Compiles the checkpoint files to generate the output of task1,2,3

    Raises:
        - `OSError` if an error occurs in reading or writing file
    """

    try:
        t1_ckpts, t2_ckpts, t3_ckpts = get_task_checkpoint_file_names()

        task_1_output = gather_task_1_results(t1_ckpts)
        task_1_a, task_1_b, task_1_c = data_op.formatted_task_1_results(
            task_1_output, config.T1_COUNT_OF_TOP_HOTTEST_DAYS
        )
        save_task_1_to_disk(
            task_1_a, task_1_b, task_1_c,
            config.T1_COUNT_OF_TOP_HOTTEST_DAYS,
            config.OUTPUT_DIR, config.T1_FILE_NAME + config.FILE_EXTENSION
        )

        gather_and_save_task_results(t2_ckpts, 2)
        gather_and_save_task_results(t3_ckpts, 3)

    except OSError as err:
        logging.error('Error occurred during processing:\n%s', str(err),
            exc_info=True)
        raise OSError from err
