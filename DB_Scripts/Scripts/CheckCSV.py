import os
import time
import pandas as pd

# Variables for the Script

STOP_TIME = 3  # Takes a Pause Between the Script
CONNECTION = 200  # Status Code = 200
ERROR = 404  # Status Code = 404


# Ensure the Directory Exists or Creates it

def create_dir(CSV_DIRECTORY):
    # If the path doesn't exist then make it.
    if not os.path.exists(CSV_DIRECTORY):
        os.makedirs(CSV_DIRECTORY)


# Function to Check if the CSV File Already Exists
def check_csv(csv_path):
    """

       :param csv_path: The csv file that will be checked if it exists or not.
       :return: Returns the csv file path location.

    """

    # Checks if the Current CSV File Exist
    return os.path.isfile(csv_path)


# Function to Initialize the CSV File
def initialize_csv(csv_path):
    """

       :param csv_path: The direct path to the csv file used in the check_csv function.
       :return: return boolean statement of "True" if the csv file doesn't exist or shuts down if the file exist.

       The main purpose of the script is to initialize the csv file path on start-up and an empty list.

       """

    if not check_csv(csv_path):
        # Create an empty CSV file only if it doesn't exist
        df_empty = pd.DataFrame()
        df_empty.to_csv(csv_path, index=False)
        print(f"Empty CSV file created at '{csv_path}'.")
        return True
    else:
        print(f"File '{csv_path}' already exists.")
        print(f"Moving On to the Next Part of the Data Mining")
        time.sleep(STOP_TIME)
