initial thoughts:
1. have some sort of validation that the URL points to a CSV file
2. don't downoad the whole file at once, it's possible that it can be
larger than the available memory
3. figure out a conflict resolution strategy if the output .txt file is
already present in the output folder
4. use Celery to distribute the three tasks on data chunks??
