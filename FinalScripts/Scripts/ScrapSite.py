import SteamCharts.Scripts.SteamChart
import FinalScripts.Scripts.MasterScript

break_time = 5
steam_scrap = SteamCharts.Scripts.SteamChart
backlogs_master = FinalScripts.Scripts.MasterScript


def steam_script():
    # Runs the script to pull the data from the requested site
    steam_scrap.scrape_and_save_to_csv(base_url='https://steamcharts.com/top',
                                       csv_file_path='\Capstone-DataAnalytics\Database\Excel\SteamCharts(Dec11).csv',
                                       start_page=1)


def backlogs_script():
    # Runs the Backlogs Master Script
    backlogs_master.master_script(back_log_url='https://www.backloggd.com/games/lib/popular/')


# First Collect the Data from Steam-charts
steam_script()
# Second Collect the Data from Backlogged
backlogs_script()
