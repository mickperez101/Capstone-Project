import langid
import requests
from bs4 import BeautifulSoup
import csv
import time
import re
import os
from DB_Scripts.Scripts.CheckCSV import initialize_csv, check_csv

"""

    PAUSE : The Break Time for the Script
    CONNECTED : Holds the Status Code for a Successful Connection
    ERROR : Holds the Status Code for a Failure Connection
    COMMENT_URL : Holds the URL Link for the website for comments
    CSV_DIRECTORY : Holds the Current Directory for the Files
    LIBRARY_CSV : Holds the File for the Merged CSV File
    LIBRARY_GAME : Holds the Column in the CSV File

"""

# Variables for the Script
PAUSE = 1
CONNECTED = 200
ERROR = 404
COMMENT_URL = 'https://www.backloggd.com/reviews/everyone/month/recent/'
CSV_DIRECTORY = r'\Capstone-DataAnalytics\Database\Excel'
LIBRARY_CSV = r'\Capstone-DataAnalytics\Database\Excel\Merged_Library(Oct12).csv'
LIBRARY_GAME = 'Game Collection'


# Function to Clean the Titles for Link Building
def clean_game_title(title):
    """
    Cleans the game title by removing unwanted characters.

    Parameters:
    - title (str): The original game title.

    Returns:
    - cleaned_title (str): The cleaned game title.
    """
    # Replace "&" with "and"
    title_conjunction = title.replace('&', 'and')
    # Replaces the normal slash with the word Slash
    title_slash = title_conjunction.replace('/', ' slash ')
    # Replace Spaces with Hyphens
    url_conversion = title_slash.replace(' ', '-')
    # Remove unwanted characters, in this case, excluding alphanumeric characters, hyphens, and spaces
    cleaned_title = re.sub(r'[^a-zA-Z0-9\s-]', '', url_conversion)
    # Replace Consecutive Hyphens with a Single Hyphen
    update_title = re.sub(r'-+', '-', cleaned_title)
    return update_title


# Function for Building the Link URL for the Games
def generate_urls(csv_file_path, column_name, base_url):
    """
    Reads Game Titles from the CSV File and Returns a List of Titles.

    Parameters:
    - csv_file_path (str): The Path to the CSV file.
    - column_name (str): The Column Name in the CSV File
    - base_url (str) : The Base URL used for Constructing Game-Specific URLs

    Returns:
    - game_collection (list): A List of Game Titles.
    - game_urls (list): A New List of URLs Constructed for Each Game
    """
    # Create Two Empty List to Store Game Titles and URL Links
    game_collection = []
    game_comment_urls = []

    # Read the CSV file
    with open(csv_file_path, 'r') as csvfile:
        # Create a CSV reader object
        csv_reader = csv.DictReader(csvfile)

        # Iterate through each row in the CSV file
        for row in csv_reader:
            # Get the game title from the specified column and add it to the list
            game_title = row[column_name]
            game_collection.append(game_title)

            # Clean the Game Title
            cleaned_title = clean_game_title(game_title)

            # Construct a New URL Link For Each Game Title
            new_url_link = (f"{base_url}"
                            f"{cleaned_title.lower()}"
                            f"/")

            game_comment_urls.append(new_url_link)

    return game_collection, game_comment_urls


# Check Network Status for the Website Links Generated
def check_url_status(urls, delay=1):
    """
    Check the status code for each URL in the list.

    Parameters:
    - urls (list): List of URLs to check.

    Returns:
    - connected_urls (list): List of URLs with a 200 status code.
    - not_found_urls (list): List of URLs with a 404 status code.
    """
    connected_urls = []
    not_found_urls = []

    for url in urls:
        response = requests.head(url)
        time.sleep(delay)
        if response.status_code == CONNECTED:
            connected_urls.append(url)
            print(f"Status {CONNECTED}: {url}. Trying the Next Link!")
        else:
            not_found_urls.append(url)
            print(f"Status 404: {url}, We could not retrieve the website")

    return connected_urls, not_found_urls


# Functions from the Second Script
def get_star_rating(stars_top):
    """

    :param stars_top: Gets the Star Rating for the Game
    :return:

    """
    if stars_top:
        style = stars_top['style']
        return int(style.split(':')[1].replace('%', '').strip()) // 20
    return None


def get_game_status(game_status_div):
    """

    :param game_status_div: Finds the Game Status
    :return:

    """
    if game_status_div:
        status_text = game_status_div.get_text(strip=True).lower()

        if 'completed' in status_text:
            return 'Completed'
        elif 'shelved' in status_text:
            return 'Shelved'
        elif 'abandoned' in status_text:
            return 'Abandoned'
    return None


# Uses an English Pattern to Only Grab English Comments
def is_english(comment):
    lang, _ = langid.classify(comment)
    return lang == 'en'


# Function handles language detection and scrapes comments from the Website
def get_comments(url, game_title):
    """
    Scrapes comments, star ratings, and game statuses for a given URL.

    Parameters:
    - url (str): The URL to scrape.
    - game_title (str): The title of the game.

    Returns:
    - comments (list): A list of dictionaries containing comment data.

    The Loop that gathers all the following information in the class_ = 'review-card'
    The Following Information is retrieved: Username, Game Title, Comment, Star Rating Status
    """

    # Check if the CSV file exists or initialize it

    comments = []
    page = 1

    while True:
        response = requests.get(url, params={'page': page})
        soup = BeautifulSoup(response.text, 'html.parser')

        review_cards = soup.find_all('div', class_='review-card')

        if not review_cards:
            print(f"No comments for: {url}")
            break

        for card in review_cards:
            # Extract the username
            username_div = card.find('div', class_='col-auto my-auto username-link pr-0 mr-n2')
            if username_div:
                username = username_div.find('p', class_='mb-0').get_text(strip=True)
            else:
                username = None

            # Extract the comment
            comment_div = card.find('div', class_='formatted-text')
            if not comment_div:
                # Some comments have "View more" and the full text is in a collapsed state
                comment_div = card.find('div', class_='collapse mb-0 card-text')
                if comment_div:
                    comment_div = comment_div.find('div', class_='formatted-text')

            if comment_div:
                comment = comment_div.get_text(strip=True)

                # Check if the comment is in English
                if is_english(comment):
                    # Get star rating
                    stars_top = card.find('div', class_='stars-top')
                    star_rating = get_star_rating(stars_top)

                    # Get game status
                    game_status_div = card.find('div', class_='game-status')
                    game_status = get_game_status(game_status_div)

                    comments.append({
                        'Username': username,
                        'Game Title': game_title,
                        'Comment': comment,
                        'Star Rating': star_rating,
                        'Status': game_status
                    })

        # Check if there is a "Load more reviews" button and extract the next page URL
        next_link_span = soup.find('span', class_='page next')
        if not next_link_span or 'aria-label' in next_link_span.a.attrs:
            # No more reviews or reached the last page
            break

        # Extract the next page URL
        next_page_url = next_link_span.a['href']
        url = f'https://www.backloggd.com{next_page_url}'

        page += 1
        time.sleep(1)  # Delay to avoid making too many requests in a short time

    return comments


def save_to_csv(comments, csv_filename):
    """
    Saves the scraped comment data to a CSV file.

    Parameters:
    - comments (list): A list of dictionaries containing comment data.
    - csv_filename (str): The filename for the CSV file.
    """

    csv_file_path = os.path.join(CSV_DIRECTORY, csv_filename)

    if check_csv(csv_file_path):
        print(f"File '{csv_filename}' already exists. Appending data.")
        mode = 'a'  # Append mode
    else:
        initialize_csv(csv_file_path)
        print(f"Creating a new file '{csv_filename}'.")
        mode = 'w'  # Write mode

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Username', 'Game Title', 'Comment', 'Star Rating', 'Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if mode == 'w':
            writer.writeheader()

        for comment in comments:
            writer.writerow(comment)


# Combine URL generation and scraping logic
def scrape_comments_for_games(csv_file_path, column_name, base_url, delay=1, max_links=None, file=None):
    """

    The Main Purpose of the function is to scrape reviews and place them into a csv file

    :param file:
    :param csv_file_path: CSV file path
    :param column_name: Name of the Column
    :param base_url: The url for the site
    :param delay: Time Delay for pinging the site
    :param max_links: Maximum number of links for the site
    :return:

    """
    game_collection, game_comment_urls = generate_urls(csv_file_path, column_name, base_url)

    connected_urls, not_found_urls = check_url_status(game_comment_urls[:max_links], delay)

    comments_data = []

    for url in connected_urls:
        game_title = game_collection[game_comment_urls.index(url)]
        comments = get_comments(url, game_title)
        comments_data.extend(comments)
        print(f"Scraped comments for: {url}")

    # Save scraped data to a CSV file
    save_to_csv(comments_data, file)

    return comments_data


def calculate_and_save_statistics(comments, csv_file):
    """
    Calculates statistics based on the collected comments for each game and saves them to a separate CSV file.

    Parameters:
    - comments (list): A list of dictionaries containing comment data.
    - csv_file (str): The filename for the CSV file.
    """
    csv_filename = csv_file
    csv_file_path = os.path.join(CSV_DIRECTORY, csv_filename)

    if check_csv(csv_file_path):
        print(f"File '{csv_filename}' already exists. Appending data.")
        mode = 'a'  # Append mode
    else:
        initialize_csv(csv_filename)
        print(f"Creating a new file '{csv_filename}'.")
        mode = 'w'  # Write mode

    with open(csv_file_path, mode, newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Game_ID', 'Game Title', 'Average Star Rating', 'Completed Percentage', 'Shelved Percentage',
            'Abandoned Percentage'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if mode == 'w':
            writer.writeheader()

        for game_id, game_title in enumerate(set(comment['Game Title'] for comment in comments), start=1):
            game_comments = [comment for comment in comments if comment['Game Title'] == game_title]

            total_reviews = len(game_comments)
            total_star_rating = sum(c['Star Rating'] for c in game_comments if c['Star Rating'] is not None)
            completed_reviews = sum(1 for c in game_comments if c['Status'] == 'Completed')
            shelved_reviews = sum(1 for c in game_comments if c['Status'] == 'Shelved')
            abandoned_reviews = sum(1 for c in game_comments if c['Status'] == 'Abandoned')

            # Calculate statistics
            average_star_rating = total_star_rating / total_reviews if total_reviews > 0 else None
            completed_percentage = (completed_reviews / total_reviews) * 100 if total_reviews > 0 else None
            shelved_percentage = (shelved_reviews / total_reviews) * 100 if total_reviews > 0 else None
            abandoned_percentage = (abandoned_reviews / total_reviews) * 100 if total_reviews > 0 else None

            # Save statistics to CSV file
            writer.writerow({
                'Game_ID': game_id,
                'Game Title': game_title,
                'Average Star Rating': average_star_rating,
                'Completed Percentage': completed_percentage,
                'Shelved Percentage': shelved_percentage,
                'Abandoned Percentage': abandoned_percentage
            })
