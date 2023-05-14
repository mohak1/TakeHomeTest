"""Contains functions to perform the tasks on the CSV data"""

import datetime
import typing as ty
from collections import defaultdict

import pandas as pd


def perform_task_1(data: pd.DataFrame, col_name, result: ty.Dict) -> None:
    """
    Task 1 consists of the following prompts:
        a. Compute the average time of hottest daily temperature (over month)
        b. Find the most commonly occurring hottest time
        c. Find the Top Ten hottest times on distinct days, sorted by date

    All of these prompts can be answered by finding out the highest
    temperature for each day and the time when that temperature occurred

    For this information, we can look at one date at a time and store
    the highest temperature and the time of highest temperature for that
    date.
    
    This function collects the highest temperature and time of highest
    temperature for each date and stores it in the `result` dict.

    Args:
        data (DataFrame): The dataframe containing CSV data
        result (dict): Variable for keeping track of the information

    The `result` dict has date string as its key and a dictionary of
    type {'temp': float, 'time': datetime} as value
    >>> Example:
    {
        '01/06/2006': {'temp': 17.2, 'time': datetime.time(15, 0)},
        '01/07/2006': {'temp': 16.0, 'time': datetime.time(8, 50)},
    }
    """
    # gather all unique dates
    unique_dates = data['Date'].unique()
    # for each date, get the max value for `col_name` and the associted time
    for date_ in unique_dates:
        temp_and_time_on_date = data.loc[
            data['Date']==date_, (col_name, 'Time')
        ]
        max_temp_val = temp_and_time_on_date[col_name].max()
        max_temp_index = temp_and_time_on_date[col_name].idxmax()
        max_temp_time = temp_and_time_on_date.loc[max_temp_index, 'Time']

        # since data is read in chunks, it's possible to have the same
        # date in more than one chunks
        if date_ in result:
            if max_temp_val > result[date_]['temp']:
                result[date_]['temp'] = max_temp_val
                result[date_]['time'] = max_temp_time
        else:
            result[date_] = {'time':max_temp_time, 'temp':max_temp_val}

def perform_task_2():
    """
    Using the "Hi Temperature" values produce a “.txt” file containing

    Collects all the Dates and Times where the “Hi Temperature” value
    is in range [21.3, 23.3] degrees (both inclusive) or the
    “Low Temperature” value is in range [10.1, 10.5] (both inclusive)
    in the first 9 days of June
    """
    raise NotImplementedError

def perform_task_3():
    """
    Forecasts “Outside Temperature” for the first 9 days of the
    next month (i.e. July), assuming that:
    a. The average daily temperature of July is 25
    b. The daily pattern of temperatures for July is the same as June.
    For instance, the pattern on July 1 is the same as the pattern on
    June 1, and so on.
    """
    raise NotImplementedError

def get_avg_time(time1: datetime.time, time2: datetime.time) -> datetime.time:
    """
    Computes and returns the average time of two datetime.time objects

    Args:
        time1 (datetime.time): first time obj
        time2 (datetime.time): second time obj

    Returns:
        (datetime.time): a datetime object of the average time
    """
    minutes1 = time1.hour * 60 + time1.minute
    minutes2 = time2.hour * 60 + time2.minute

    avg_minutes = (minutes1 + minutes2) // 2

    avg_hours = avg_minutes // 60
    avg_minutes = avg_minutes % 60

    return datetime.time(avg_hours, avg_minutes)

def avg_time_of_hottest_daily_temp(result: ty.Dict) -> ty.List[ty.Tuple]:
    """
    Loops over the elements of the input dictionary. For each
    mm/yyyy, calculates the averate of the daily hightest temperatures

    Assumes the input dict keys to be strings in dd/mm/yyyy format

    Args:
        result (dict): dictionary with format of task 1 output, i.e. a 
        dictionary of dictionaries where each element of the dictionary
        is of the format:
        {
            '01/06/2006': {'temp': 17.2, 'time': datetime.time(15, 0)},
            '01/07/2006': {'temp': 16.0, 'time': datetime.time(8, 50)},
        }

    Returns:
        avg_hottest_times (list): a list of tuples where each tuple
        contains month as first value and average time of hottest
        temperature as the second value, eg:
        [('05/2006', '14:40'), ('06/2006', '12:33'),]
    """
    avg_hottest_time = {}
    for key in result:
        mm_yyyy = key[3:] # key is '31/05/2006'
        if mm_yyyy in avg_hottest_time:
            avg_hottest_time[mm_yyyy] = get_avg_time(
                avg_hottest_time[mm_yyyy], result[key]['time']
            )
        else:
            avg_hottest_time[mm_yyyy] = result[key]['time']

    # convert the dict to list of tuples and convert time to string
    values_as_list = [
        (i[0], i[1].strftime('%H:%M')) for i in avg_hottest_time.items()
    ]
    return values_as_list

def hottest_time_with_hightest_freq(result: ty.Dict) -> str:
    """
    Loops over the elements of the input dictionary. Counts the
    frequency of each time object and maintains this count in the
    `freq_count` dictionary.
    Loops over the `freq_count` dictionary and finds the time that has
    the maximum frequency. In case of a tie, it returns the value that
    was encountered first

    Args:
        result (dict): dictionary with format of task 1 output, i.e. a 
        dictionary of dictionaries where each element of the dictionary
        is of the format:
        {
            '01/06/2006': {'temp': 17.2, 'time': datetime.time(15, 0)},
            '01/07/2006': {'temp': 16.0, 'time': datetime.time(8, 50)},
        }

    Returns:
        time_val (str): 'HH:MM' time that has highest frequency in input
    """
    freq_count = defaultdict(int)

    # count the frequency of each 'time' object
    for ele in result:
        time_obj = result[ele]['time']
        freq_count[time_obj] += 1

    max_freq = 0
    time_with_max_freq = None

    # return the time with max frequency
    for time in freq_count:
        if freq_count[time] > max_freq:
            max_freq = freq_count[time]
            time_with_max_freq = time

    time_val = time_with_max_freq.strftime('%H:%M')
    return time_val

def top_hottest_times(result: ty.Dict, count: int) -> ty.List[ty.Tuple]:
    """
    Sorts the `result` dictionary by both 'temp' and date (key).
    The temperature is sorted in descending order while the date is
    sorted in the ascending order. For this, the sorting in the
    ascending order using negative dates.

    The top `count` elements are taken from the sorted list and are
    converted to string then returned.

    Args:
        result (dict): dictionary with format of task 1 output, i.e. a 
        dictionary of dictionaries where each element of the dictionary
        is of the format:
        {
            '01/06/2006': {'temp': 17.2, 'time': datetime.time(15, 0)},
            '01/07/2006': {'temp': 16.0, 'time': datetime.time(8, 50)},
        }

        top_count (int): the number of top values to return

    Returns:
        top_temp_and_dates (list): a list of tuples containing the top
        temperatures (as string) and dates, eg:
        [('23.2', '06/06/2006'), ('22.4', '11/06/2006'),]
    """

    # sorting ascending based on -ve value of `temp` and date (i.e. key)
    # this results in `temp` being sorted in descing order
    # and date being sorted in ascending order
    # result.items() -> tuple(key, {'temp':num, 'time': date_obj})
    # `item[1]['temp']` is the temp value (taken as -ve)
    # `item[0]` is the key (i.e. date string)
    sorted_result = sorted(
        result.items(), key=lambda item: (-item[1]['temp'], item[0])
    )

    # take the top `count` elements
    top_elements = sorted_result[:count]

    # conver to list of tuples (of strings) for ease of writing to disk
    top_temp_and_dates = [
        (str(i[1]['temp']), i[0]) for i in top_elements
    ]

    return top_temp_and_dates
