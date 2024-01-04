import pandas as pd
from BackLogs.BLScripts.BL_Comment import check_csv, initialize_csv


def compare_and_calculate(file1, file2, output_path, print_message=False):
    # Check if the CSV file already exists
    if check_csv(output_path):
        # If the CSV file exists, print a message
        if print_message:
            print(f"Data loaded from existing CSV file '{output_path}'")
        return output_path

    else:
        # Creates a New CSV File If It Does Not Exist
        initialize_csv(output_path)

    # Load the first CSV file (SteamCharts(Dec11).csv)
    df_steam = pd.read_csv(file1)

    # Load the second CSV file (Merged_Library(Oct11).csv)
    df_library = pd.read_csv(file2)

    # Merge the two dataframes based on the 'Title' column
    merged_df = pd.merge(df_steam, df_library, left_on='Title', right_on='Game Collection', how='inner')

    # Calculate the change in Total Hours
    merged_df['Total Hours Change(Oct-Dec)'] = merged_df['Total Hours'] - merged_df['Total Hours Spent']

    # Calculate the ratio of player to hours for SteamCharts(Dec11).csv and Merged_Library(Oct11).csv
    merged_df['Ratio Steam(Oct)'] = merged_df['Total Hours Spent'] / (merged_df['Current Player '
                                                                                'Count'] + merged_df['Peak Player '
                                                                                                     'Count'])

    merged_df['Ratio Steam(Dec)'] = merged_df['Total Hours'] / (merged_df['Current Players'] + merged_df['Peak '
                                                                                                         'Players'])

    merged_df['Ratio Change(Oct-Dec)'] = merged_df['Ratio Steam(Dec)'] - merged_df['Ratio Steam(Oct)']

    # Determine positive or negative change
    merged_df['Change Type'] = ['Positive' if change > 0 else 'Negative' for change in merged_df[('Total Hours Change'
                                                                                                  '(Oct-Dec)')]]
    merged_df['Change Ratio'] = ['Positive' if change > 0 else 'Negative' for change in merged_df[('Ratio Change'
                                                                                                   '(Oct-Dec)')]]

    # Save only the calculated values to a new CSV file
    output_df = merged_df[['Title', 'Total Hours Change(Oct-Dec)', 'Change Type', 'Ratio Steam(Oct)',
                           'Ratio Steam(Dec)', 'Ratio Change(Oct-Dec)', 'Change Ratio']]
    output_df.to_csv(output_path, index=False)

    if print_message:
        print(f"Data saved to '{output_path}'")


# Comparing the CSV Files
file_name1 = r'\Capstone-DataAnalytics\Database\Excel\SteamCharts(Dec11).csv'
file_name2 = r'\Capstone-DataAnalytics\Database\Excel\Merged_Library(Oct11).csv'
output_file = r'\Capstone-DataAnalytics\Database\Excel\Results.csv'

compare_and_calculate(file_name1, file_name2, output_file, print_message=True)
