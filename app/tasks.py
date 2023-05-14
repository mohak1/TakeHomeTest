"""Contains functions to perform the tasks on the CSV data"""

import typing as ty

import config
import pandas as pd


def perform_task_1(data: pd.DataFrame, result: ty.Dict) -> None:
    """
    Performs the following operations on the specified column:
        a. Computes the average time of hottest daily temperature (over month)
        b. Finds the most commonly occurring hottest time in a day
        c. Finds the Top Ten hottest times on distinct days, sorted by date
    
    Updates the `result` dictionary with the output of the operation

    Args:
        data (DataFrame): The dataframe containing CSV data
        result (dict): Variable for keeping track of the obtained result

    """
    # gather all unique dates
    unique_dates = data['Date'].unique()
    col_name = config.T1_COL_NAME
    # for each date, get the max outside temp and the associted time
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
