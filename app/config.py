"""
This file contains constants and other configuration values that are
used in the code
"""
import datetime

# TODO: replace column name string values with ENUMs

URL = 'http://www.fifeweather.co.uk/cowdenbeath/200606.csv'
CHUNK_SIZE = 1024
OUTPUT_DIR = './output'
T1_FILE_NAME = 'task1'
T2_FILE_NAME = 'task2'
T3_FILE_NAME = 'task3'
FILE_EXTENSION = '.txt'
SAVE_CKPT_EVERY = 1 # save result checkpoint after every 1 iteration

# column names that are required in the CSV file for the tasks
EXPECTED_COL_NAMES = [
    'Date', 'Time', 'Outside Temperature', 'Hi Temperature',
    'Low Temperature',
]

# columns from EXPECTED_COL_NAMES that are expected to have numeric data
NUMERIC_COL_NAMES = [
    'Outside Temperature', 'Hi Temperature', 'Low Temperature',
]

# constants used for Task 1
T1_COL_NAME = 'Outside Temperature'
T1_COUNT_OF_TOP_HOTTEST_DAYS = 10

# constants used for Task 2
T2_START_DATE = datetime.datetime.strptime('01/06/2006', '%d/%m/%Y')
T2_END_DATE = datetime.datetime.strptime('09/06/2006', '%d/%m/%Y')
T2_COL_VALUE_RANGE = [
    # column name, range start value, range end value (both inclusive)
    ('Hi Temperature', 21.3, 23.3),
    ('Low Temperature', 10.1, 10.5),
]

# constants used for Task 3
T3_FORECAST_COL_NAME = 'Outside Temperature'
T3_AVERAGE_TEMP = 25
