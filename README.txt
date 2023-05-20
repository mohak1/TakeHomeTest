## Work in progress ##

========================================================================
Initial thoughts for version 2 (mitigating shortcomings of version 1)
========================================================================
This version builds upon the shortcomings of the previous implementation
in an attempt to make the script more robust and flexible.

Improvements planned in this version:

1. Using Celery for performing task 1, 2, and 3 in parallel in order to
    boost the overall performance.

2. Creating a process for storing the intermediate results of the tasks
    as checkpoints. The implementation in version 1 stores the output
    of each data chunk in the memory until all the chunks are
    processed. This puts a limit on the size of the resource that the
    script can handle.
    In this version, the intermediate results will be stored to disk
    after every 'n' number of chunks. This will enable the script to be
    used for very large data.

-> these checkpoint filds will be combined together to form the final
    output after all the data chunks are processed

-> can create a logic that scans the output dir for checkpoints and
    figures out which chunks are missing, then downloads the missing
    chunks. This will be useful in case of data corruption

3. Consistency on the type of methods that raise an error (when the
    exception is not recoverable) and the methods that exit the process
    when an unrecoverable error occurs.
    Currently, there are multiple methods that perform sys.exit() when
    faced with an unrecoverable error. This should be changed to
    increase re-usability of the code.
    Only the top level method should perform sys.exit() while all other
    internal methods should raise exceptions.

4. Increasing the number of config variables that can be changed by
    command line arguments. This will make it easy to use the script
    in a number of places without the need of changing the config.py
    file for every individual operation.

-> a number of validation methods will be required for this. And will
    need to make a decision for the level of checks to be performed
    in the validator method. i.e. when updating the resource url, the
    scrictness of the validation check could range from just checking
    if the input is a non-numeric string, all the way up to checking if
    the url points to a valid address on the internet

5. Improving the use of logging and increasing the tests


========================================================================
How to run the code
========================================================================
1. Clone this project:
    `git clone https://github.com/mohak1/TakeHomeTest.git`
2. cd into the `TakeHomeTest` directory:
    `cd TakeHomeTest`
3. Create a virtual environment env:
    `python3 -m venv env`
4. Activate the virtual environment env:
    `source env/bin/activate`
5. Install the required pip packages:
    `pip install -r requirements.txt`
6. Start docker daemon
7. Start a RabbitMQ server in a docker container on port 5672:
    `docker run -d --name rabbitmq -p 5672:5672 rabbitmq`
8. Start the Celery worker:
    `celery -A app.tasks worker --loglevel=info`
9. Run the main.py file in a different terminal window:
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
