TODO: change the README from .txt to .md
TODO: add the sections:
    - how to run
    - assumptions made
    - design choices and decisions
TODO: add GitHub Actions CI to run the test suite; add Discord notifs

initial thoughts:
1. have some sort of validation that the URL points to a CSV file
2. don't downoad the whole file at once, it's possible that it can be
    larger than the available memory
3. figure out a conflict resolution strategy if the output .txt file is
    already present in the output folder
4. use Celery to distribute the three tasks on data chunks??

project structure:
- using `flat layout` with all the files inside the `app` directory and
    `requirements.txt` outside the `app` folder to keep things organised
- using `config.py` for storing all the constants like URL, etc


========================================================================
-> Pandas dataframes?
-> return iterators of data chunks?
========================================================================
Convert the Date column values to a datetime object and check for day
and month values

========================================================================
Task1:
- use "date" and "outside temperature" column values
- a. keep track of the daily average temperatures
- b. keep track of the hottest time for each day and its frequency
- c. sort the dict in 'b' wrt time; grab the top 10

NOTE: read the column names (i.e. "date", "outside temperature") from
    config.py; maybe also allow it to be changed from the
    arguments (?)

# assumption: storing info of each day in a dict assuming that num days
are not large enough to cause MemoryError
# can be handled by saving the daily average/hottest info to disk
    after processing x num of years or x num of rows hence clearing the
    memory; then reading these files one at a time for generating the
    final answer; implementing this approach in the current solution
    would be an overkill
========================================================================
Task2:
- use "hi temperature" and "low temperature" column values
- write to file if "hi temperature" is in the range [21.3, 23.3]
- write to file if "low temperature" is in the range [10.1, 10.5] for
    the first 9 days of June

NOTES:
    - read column names, their temperature ranges and date range i.e.
        "x days of month" from config.py like:
            `{col_name: valid_temp_range}`
            `date_range_start` and `date_range_end`
    - write to file only once if both of these conditions are true like:
        ```
        if date_range_start <= date <= date_range_end:
            for col_name, col_temp in row:
                if is_in_valid_range(col_name, col_temp):
                    # write to file
        ```
========================================================================
Task3:
- use the "date" and "outside temperature" column values
- calculate the mean and standard deviation of temparatures in June and
    assume that the values follow a normal distribution
- since July follows the same pattern as June and has a mean of 25,
    assume a normal distribution of temperatures and generate the values
    for the first 9 days

NOTES:
    - read column name, date range, average temperature from config.py
    - read up on normal distribution and explore if a better approach
        exists; since it is not guaranteed that June temperature values
        will follow a normal distribution
========================================================================
