import os
import re
import sys
import time
import pandas as pd
import html
import requests

# Variables for the Script

STOP_TIME = 1  # Takes a Pause Between the Script
CONNECTION = 200  # Status Code = 200
ERROR = 404  # Status Code = 404

# Other Important Information
LIBRARY_URL = 'https://www.backloggd.com/games/lib/popular/'  # URL Link
CSV_DIRECTORY = r'\Capstone-DataAnalytics\Database\Excel'  # CSV Path Directory
english_title_pattern = r'^[A-Za-z0-9 !@#$%^&*()_+-=[\]{}|:;"\'<>,.?/]+$'  # Pattern For English Text

# Ensure the Directory Exists or Creates it
if not os.path.exists(CSV_DIRECTORY):
    os.makedirs(CSV_DIRECTORY)  # If the path doesn't exist then make it.


# Start Up: Initial Connection

def connection_status(status_code):
    if status_code == CONNECTION:
        print(f"Successfully Connected, Status Code = {CONNECTION}")
        time.sleep(STOP_TIME)
    elif status_code == ERROR:
        print(f"No Connection, Status Code = {ERROR}")
        time.sleep(STOP_TIME)
        print(f"Ending Program")
        sys.exit()
    else:
        print(f"Unexpected Status Code: {status_code} or Program Has An Error")
        time.sleep(STOP_TIME)
        print("Ending Program")
        sys.exit()


def start_up_message():
    print("Beginning to Collect All Game Titles On the Site")
    time.sleep(STOP_TIME)


# Function to Check if the CSV File Already Exists

def check_csv(csv_path):
    return os.path.isfile(csv_path)


# Function to Check the Connection Status

def check_status(url):
    response = requests.get(url)
    status_code = response.status_code
    return status_code, response


# Function to Grab the BackLog Library
def game_collection(LIBRARY_URL, csv_path, game_lib):
    if check_csv(csv_path):
        print(f"File '{csv_path}' already exists. Skipping scraping.")
        return game_lib  # Skip scraping and continue with the script

    status_code, response = check_status(LIBRARY_URL)

    if status_code != CONNECTION:
        print(f"Failed to request the Page and popped up with {ERROR}")
    else:
        back_content = response.text
        title_pattern = r'<div class="game-text-centered">([^<]*)</div>'
        title_matches = re.findall(title_pattern, back_content)
        title_matches = [html.unescape(game_title) for game_title in title_matches if
                         re.match(english_title_pattern, game_title)]
        game_lib.extend(title_matches)

    return game_lib


# Encapsulated while loop in a function
def scrape_pages(start_page, page_limit, library_url, csv_directory, backlog_file):
    # Check the Connection Status to the Website
    status_code, response = check_status(LIBRARY_URL)
    connection_status(status_code)
    start_up_message()

    page_num = start_page
    game_lib = []
    csv_file = os.path.join(csv_directory, backlog_file)  # Initialize csv_file outside the loop

    while page_num <= page_limit:
        current_url = f"{library_url}?page={page_num}"
        status_code, response = check_status(current_url)

        if status_code == CONNECTION:
            print(f"Beginning to Scrape Page # {page_num}")

            # Use the existing csv_file instead of redefining it here
            game_lib = game_collection(current_url, csv_file, game_lib)

            if game_lib:
                for title in game_lib:
                    print(title)

                page_num += 1
                time.sleep(STOP_TIME)

            else:
                print(f"No more entries on Pages. Exiting and Moving On.")
                break  # Move the break statement here
        else:
            print(f"Unexpected Status Code: {status_code} or Program Has An Error")
            time.sleep(STOP_TIME)
            print("Ending Program")
            sys.exit()

    # Create a Data Frame and Save the DataFrame to a CSV file after scraping all pages
    df = pd.DataFrame({'Game Title': game_lib})

    # Use mode='a' to append to the existing file if it exists
    df.to_csv(csv_file, mode='a', header=not os.path.exists(csv_file), index=False)
    print(f"Data appended to '{csv_file}'")
