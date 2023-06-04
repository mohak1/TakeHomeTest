========================================================================
New in version 2
========================================================================
1. Task distribution with worker threads using Celery and RabbitMQ

2. Saving intermediate progress as checkpoints to disk

3. Logging method execution flow to make debugging easier

4. The ability to change config values using command line arguments

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
9. Open a different terminal window, activate env and run main.py:
    `python app/main.py`

========================================================================
Design Choices and Decisions
========================================================================
1. Distributing task execution using Celery and RabbitMQ
    The tasks are independent of each other and certainly benefit from
    parallel execution. The performance improvements will be significant
    the tasks are run on larger data chunks or if the tasks are updated
    and made more complex.

2. The choice between worker threads and processes for Celery
    In the current implementation, Celery is using worker threads
    instead of worker processes even though the threads are restricted
    by GIL in CPython.
    The average runtime with Celery worker threads was `0.8738 sec` and
    with worker processes was `1.6535 sec` (average of 5 runs each).
    The worker processes were slower than threads, even though they
    had not GIL restriction and achieved true parallelism. This could
    be because the time required to set up memory spaces for processes
    if far greater than the time required to complete the tasks. Hence
    threads offer better performance and are chosen as Celery workers.

3. Catching exceptions in main() using a decorator
    Since the error handling mechanism is the same for all the raised
    exceptions in main(), i.e. exiting the script with sys.exit(),
    using a decorator for exceptions is a lot cleaner approach.
    If different exceptions were to be handled differently, using
    multiple try-except blocks in main() woud have been the most
    approapriate choice.

4. Saving checkpoints as pickle binary files rahter than text files
    This is because pickle files can store data structures instead of
    just text. This removes the intermediate step of converting the
    data structure values to strings (when saving checkpoints) and
    converting strings to data structures (when reading checkpoints).
    Also, binary files are more compact and require less space on the
    disk then text files.

========================================================================
Future considerations and improvements
========================================================================
1. Solving Task 1 using SQL
    Currently, all Task 1 checkpoints are gathered in one dictionary
    to compute the results for subtasks a, b, and c.  This is because
    the frequency of occurrence of different temperatures and date
    values is needed to answer these subtasks.
    By storing the task 1 checkpoints in an SQL table, these subtasks
    can be easily answered using SQL queries. This will also improve
    the performance.

2. A step to look for missing checkpoints and generate them
    The current implementation creates the checkpoint files after a
    fixed number of data chunks are processed. These checkpoints are
    later used for generating the output.
    When operating on large data, the code will generate a lot of
    checkpoint files and there is a possibility that a couple of files
    might get corrupted/deleted due to disk errors. Hence the script
    should have a step to verify that all the checkponits are present
    before generating the final output using these checkpoints.
    In addition, a step to download these missing checkpoints would also
    make the script very robust.

3. Caching on GitHub Actions to improve CI time
    By default, GitHub deletes all the resources after the completion
    of a CI/CD action. Due to this, every time a Git Action is run, the
    requirements are downloaded and installed. While this is perfectly
    fine when the dependencies are light, this can become a time
    consuming step as the dependencies grow.
    One solution is to cache the downloaded pip wheels. But implementing
    caching on GitHub Actions can be a bit complicated, so it is a good
    option when downloading dependencies starts taking very long.
