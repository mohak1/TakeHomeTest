## Work in progress ##
    - how to run
    - assumptions made
    - design choices and decisions

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

-> Why downloading the data in chunks from the URL?
This decisions is influenced by the initial conversation that the role
involves working with data that can be Petabites in magnitude.
Since that's the case, the approach of downloading the data chunk by
chunk enables this script (or at least a part of it) to be used
for data thats very large and can't fit in the memory.

Also this way we have a better fault isolation mechanism. If something
unexpected happens during the processing of one of one chunk, we can
either halt the script or save a checkpoint file with all the current
progress before terminating the script. However, fault tolerance is not
implemented in the current version of the code.


-> Why Pandas dataframes?
The decision to use pandas dataframes for performing the operations on
the CSV data is inspired by the idea of having very large data.
Operations performed using Pandas inbuilt methods are significantly
faster due to its CPython implementation. Hence, it can help in
achieving massive performance gains when dealing with large data.


--updating--
========================================================================
