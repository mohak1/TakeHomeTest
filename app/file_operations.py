"""Contains functions for performing file read/write operations"""

import typing as ty
import validator

def save_task_1_to_disk(
    task_1_a_result: ty.List[ty.Tuple],
    task_1_b_result: str,
    task_1_c_result: ty.List[ty.Tuple],
    top_count_value: str,
    dir_path: str,
    file_name: str,
) -> None:
    """
    Opens `file_name` at `path` with mode `a` and appends to the
    contents of the file. Creates a new file if the file doesn't exist

    Args:
        path (str): path of the dir where file is to be saved
        file_name (str): name of the file to be saved
        data (str): the data to be appended to the file

    Raises
        # TODO: add exception info
    """
    task_1_a_heading = 'Average time of hottest daily temperature (over month)'
    task_1_b_heading = 'Most commonly occurring hottest time of day'
    task_1_c_heading = f'Top {top_count_value} hottest times on distinct days'

    validator.validate_dir_path(dir_path)

    with open(file=f'{dir_path}/{file_name}', mode='a', encoding='utf-8') as file:
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
