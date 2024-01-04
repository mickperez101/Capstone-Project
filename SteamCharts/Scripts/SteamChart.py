from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import os

# Status Codes
COMPLETE = 200  # 200 code means it connected.
FAIL = 404  # 404 code means it failed to connect.

# The URL Link for SteamCharts.com
STEAM_URL = 'https://steamcharts.com/top'
BASE_URL = STEAM_URL

# Wait Time Variable Between Each Request
WAIT_TIME = 0
TIME_BREAK = 0

# Stored Data Scraped from the Website
Data_set = []

# Directory where you want to save the CSV file
CSV_DIRECTORY = '\Capstone-DataAnalytics\Database\Excel'


# Function to scrape data and save to CSV
def scrape_and_save_to_csv(base_url, csv_file_path, start_page=1):
    # Check if the CSV file already exists
    if os.path.exists(csv_file_path):

        # Read existing data from CSV file to Data_set

        print(f"CSV file found. Appending data to the existing file.")

        return

    else:
        # Creates a New CSV File if it does not exist
        print(f"CSV file not found. Creating a new one.")
        # Create an empty DataFrame with the same columns
        df_empty = pd.DataFrame(columns=['ID', 'Rank', 'Title', 'Current Players', 'Peak Players', 'Total Hours'])
        df_empty.to_csv(csv_file_path, index=False)
        data_set = []

    num_pages = start_page

    while True:
        steam_url = f"{base_url}/p.{num_pages}"
        response = requests.get(steam_url)

        if response.status_code == COMPLETE:
            print(f"Beginning to Scrape Page # {num_pages}")
            data_set.extend(scraping_data(steam_url, len(data_set)))
            num_pages += 1
            time.sleep(WAIT_TIME)
        else:
            print(f"No more pages to be scraped. Transferred to the CSV file")
            break

    # Convert the data_set list to a DataFrame
    df = pd.DataFrame(data_set, columns=['ID', 'Rank', 'Title', 'Current Players', 'Peak Players', 'Total Hours'])

    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)
    print(f"Data saved to '{csv_file_path}'")


# A Function to Scrape the Data from the Website
def scraping_data(steam_url, id_counter):
    data_set = []
    # Sends an HTTP Get request to the URL
    steam_response = requests.get(steam_url)

    if steam_response.status_code != COMPLETE:
        print(f"Failed to request the Page and popped up with {FAIL}")
    else:
        print(f"Successfully Connected to the Page and Status Code = {COMPLETE}")
        time.sleep(TIME_BREAK)
        print(f"Will Begin Scrapping Data from Page 1 after 5 seconds")
        time.sleep(TIME_BREAK)

        # Defines webpage to parse the HTML content with Beautiful Soup
        steam_soup = BeautifulSoup(steam_response.content, "html.parser")
        # Find the table containing our data
        s_table = steam_soup.find("table", {"class": "common-table"})
        # Find the rows in our data set and Skip the Header Values
        s_rows = s_table.find_all("tr")[1:]

        # Pulls Defined Variables to Represent Each Column of the Data Set
        for row in s_rows:
            # Game Rank Column
            rank_column = row.find_all("td")
            # Game Title Column
            title_column = row.find_all("td", {"class": "game-name left"})
            # Current Players Column
            num_column = row.find_all("td", {"class": "num"})
            # Peak Number Column
            peak_column = row.find_all("td", {"class": "num period-col peak-concurrent"})
            # Hours Played Ongoing Column
            hour_column = row.find_all("td", {"class": "num period-col player-hours"})

            # Takes the List from the Top Ranking to Lowest Ranking
            rank = rank_column[0].text.strip()
            # Input the Title of the Game
            title = title_column[0].text.strip()
            # Input the Current Player Count
            current = num_column[0].text.strip()
            # Input Peak Players Count
            peak = peak_column[0].text.strip()
            # Input Hours Played
            hour = hour_column[0].text.strip()

            # Append the data to the data_set list
            data_set.append([id_counter, rank, title, current, peak, hour])
            id_counter += 1  # Increment the ID counter

            # Prints the Results of the Columns
            print(
                f"ID: {id_counter}, Rank: {rank}, Game: {title},"
                f" Current Players: {current}, "
                f"Peak Players: {peak}, "
                f"Hours Played: {hour}"
            )

    return data_set
