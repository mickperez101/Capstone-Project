"""

    The master script combining the following scripts:

    - BL_Comment.py
    - BL_Library.py
    - MergeCSV.py

    Runs all related functions for the script to be performed on one script.

"""

import os
from BackLogs.BLScripts.BL_Library import scrape_pages
from BackLogs.BLScripts.MergeCSV import merge_csv_files
from BackLogs.BLScripts.BL_Comment import scrape_comments_for_games, calculate_and_save_statistics

# CSV Filename Variables and They can be Changed

back_logs_collection = 'BackLogs_Library.csv'
steam_chart_file = 'SteamCharts.csv'
back_log_file = 'Backlog_Reviews(Dec11).csv'
game_statistic_file = 'Stats_Analysis.csv'
merged_csv_file = 'Merged_Library(Oct11).csv'


def master_script(back_log_url):
    # BL_Library script
    csv_directory = '\Capstone-DataAnalytics\Database\Excel'
    comment_url = 'https://www.backloggd.com/reviews/everyone/week/recent/'
    bl_library_csv_path = os.path.join(csv_directory, back_logs_collection)
    scrape_pages(start_page=1, page_limit=1, library_url=back_log_url,
                 csv_directory=csv_directory, backlog_file=back_logs_collection)

    # MergeCSV script
    steam_charts_csv_path = os.path.join(csv_directory, steam_chart_file)
    merge_csv_output_path = os.path.join(csv_directory, merged_csv_file)
    merged_file_path = merge_csv_files(steam_charts_csv_path, bl_library_csv_path, merge_csv_output_path)
    print(f"Merging completed. Check '{merged_file_path}' for the result.")

    # BL_Comment script
    library_csv_path = os.path.join(csv_directory, merge_csv_output_path)
    comments_output_path = os.path.join(csv_directory, back_log_file)
    comments_data = scrape_comments_for_games(library_csv_path, 'Game Collection', comment_url, delay=0.5,
                                              max_links=5194, file=comments_output_path)
    calculate_and_save_statistics(comments_data, game_statistic_file)

    print(f"Scraping comments completed. Check '{comments_output_path}' and statistics are saved from the results.")
