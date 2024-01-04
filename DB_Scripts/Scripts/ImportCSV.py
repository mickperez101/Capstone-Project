import sqlite3
import pandas as pd
from DB_Scripts.Scripts.CreateDB import library, stat, review

"""
    Description of the Script: The purpose of the script is meant to import the data
    stored on the Excel file from the initial scrapped site to a SQLite database. This
    script will also be used to manipulate the database for SteamCharts.

"""

# Database Connection for Scrapping Sites Database

connection = sqlite3.connect(r'/Capstone-DataAnalytics/Database/SQLite/ScrappingSites.db')
cursor = connection.cursor()


# Function will Transfer the Data from the file to Database Created.
def transfer_data(steam_file, name, connection):
    # Takes the BackLog Comment File and Uploads to the Database
    df = pd.read_csv(steam_file)
    df.columns = df.columns.str.strip()

    df.to_sql(name, connection, if_exists='replace')

    print(f'Transfer Complete for {steam_file}')


def back_transfer(back_file, name, connection):
    # Takes the BackLog Comment File and Uploads to the Database
    bg = pd.read_csv(back_file)
    bg.columns = bg.columns.str.strip()

    bg.to_sql(name, connection, if_exists='replace')

    print(f'Transfer Complete for {back_file}')


def stats_transfer_data(stat_file, name, connection):
    # Takes the Statistic File and Uploads to the Database
    ss = pd.read_csv(stat_file)
    ss.columns = ss.columns.str.strip()

    ss.to_sql(name, connection, if_exists='replace')

    print(f'Transfer Complete for {stat_file}')


transfer_data(steam_file=r'\Capstone-DataAnalytics\Database\Excel\SteamCharts(Dec11).csv',
              name=library, connection=connection)

back_transfer(back_file=r'\Capstone-DataAnalytics\Database\Excel\Backlog_Reviews(Dec11).csv',
              name=review, connection=connection)

stats_transfer_data(stat_file=r'\Capstone-DataAnalytics\Database\Excel\Stats_Analysis.csv',
                    name=stat, connection=connection)

connection.commit()
connection.close()
