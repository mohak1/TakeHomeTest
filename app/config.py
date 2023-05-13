"""
This file contains constants and other configuration values that are
used in the code
"""
import datetime

# TODO: replace column name string values with ENUMs

URL = 'http://www.fifeweather.co.uk/cowdenbeath/200606.csv'
OUTPUT_DIR = ''
T1_FILE_NAME = ''
T2_FILE_NAME = ''
T3_FILE_NAME = ''
EXPECTED_COL_NAMES = {} # column names that the CSV file should have

# constants used for Task 1
T1_COL_NAME = 'Outside Temperature'

# constants used for Task 2
T2_START_DATE = datetime.datetime.strptime('01-06-2006', '%d/%m/%Y')
T2_END_DATE = datetime.datetime.strptime('09-06-2006', '%d/%m/%Y')
T2_COL_TEMP_RANGE = {
    'Hi Temperature': (21.3, 23.3),
    'Low Temperature': (10.1, 10.5),
}

# constants used for Task 3
T3_COL_NAME = 'Outside Temperature'
AVERAGE_TEMP = 25
T3_NUM_DAYS = 9
