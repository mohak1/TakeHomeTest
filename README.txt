========================================================================
How to run the code
========================================================================
1. Clone this project
2. cd into the TakeHomeTest directory
3. Create a virtual environment by running:
    `python3 -m venv env`
4. Activate the virtual environment by running:
    `source env/bin/activate`
5. Install the requirements by running:
    `pip install -r requirements.txt`
6. Run the main.py file by using the command:
    `python app/main.py`

========================================================================
Design Choices and Decisions
========================================================================

1. Downloading the data in chunks from the URL
    This decisions is influenced by the initial conversation that the
    role involves working with data that can be Petabites in magnitude.
    Since that's the case, the approach of downloading the data chunk by
    chunk enables this script (or at least a part of it) to be used
    for data thats very large and can't fit in the memory.

    Also this way we have a better fault isolation mechanism. If
    something unexpected happens during the processing of one of one
    chunk, we can either halt the script or save a checkpoint file with
    all the current progress before terminating the script. However,
    fault tolerance is not implemented in the current version of the
    code.

2. Using Pandas dataframes
    The decision to use pandas dataframes for performing the operations
    on the CSV data is inspired by the idea of having very large data.
    Operations performed using Pandas inbuilt methods are significantly
    faster due to its CPython implementation. Hence, it can help in
    achieving massive performance gains when dealing with large data.

3. The use of GitHub Actions was a way of ensuring the consistency of
    the script. The tests execute when Pull Requests are created and
    can identify failing test cases without the need of merging into
    the branch.

========================================================================
Future considerations and improvements
========================================================================
1. Since the tasks (Task1, Task2, Task3) are unrelated and independent
    from each other, they can be processed separately.
    I wanted to try unloading these tasks with Celery using RabbitMQ
    but ran out of time.

2. In order to make this script highly customisable, I wanted to add
    multiple command line arguments using argparse for changing almost
    every variable in config.py
    The only trouble with this approach was that it required a number
    of validator methods to ensure they are of the expected type.
    I tried to designed this script in a way where it could either be
    used in a loop (processing different URLs and saving them in
    different files) by passing different command line arguments.
    Unfortunately the script didn't quite reach there.

3. An important considerations while designing this script was the size
    of the data. Even though the current script does not download the
    entire file at once and neither does it make deepcopies of the data,
    it still stores the intermediate outputs in the memory at all times.
    In the main method, `task_1_output`, `task_2_output`, `task_3_output`
    variables are used to store the output of tasks. This is problematic
    as its likely that these variables can grow in size and, if the
    data is large enough, can easily fill up the entire available memory.
    To solve this, there can be a mechanism to save 'checkpoints' after
    a number of iterations (or depending on the variable size).
    This would help in avoiding memory error.

4. The script can certainly benefit from more logging. Also adding more
    tests would be beneficial, specially ones with edge cases.
