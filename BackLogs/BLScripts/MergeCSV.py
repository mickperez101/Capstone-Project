import pandas as pd
from BackLogs.BLScripts.BL_Comment import check_csv, initialize_csv


def merge_csv_files(file1, file2, output_path, print_message=False):
    # Check if the CSV file already exists
    if check_csv(output_path):
        # If the CSV file exists, print a message
        if print_message:
            print(f"Data loaded from existing CSV file '{output_path}'")
        return output_path

    else:
        # Creates a New CSV File If It Does Not Exist
        initialize_csv(output_path)

    print(f"Loading CSV files: {file1}, {file2}")

    # Load the first CSV file
    df1 = pd.read_csv(file1)

    # Load the second CSV file
    df2 = pd.read_csv(file2)

    print(f"Columns in df1: {df1.columns}")
    print(f"Columns in df2: {df2.columns}")

    # Merge the two dataframes based on the 'Title' column in the first DataFrame
    # and 'Game Title' column in the second DataFrame using an inner join
    merged_df = pd.merge(df1, df2, left_on='Title', right_on='Game Title', how='inner')

    print(f"Merged DataFrame:\n{merged_df.head()}")

    # Print the titles and ranks that match
    matching_data = merged_df[['Title', 'Rank', 'Current Players', 'Peak Players', 'Total Hours']]
    print(f"Matching Titles and Ranks:\n{matching_data}")

    # Drop duplicates based on the 'Title' column
    merged_df = merged_df.drop_duplicates(subset='Title')

    # Rename the 'Title' column to 'Game Collection'
    merged_df = merged_df.rename(columns={'Title': 'Game Collection', 'Current Players': 'Current Player Count',
                                          'Peak Players': 'Peak Player Count', 'Total Hours': 'Total Hours Spent'})

    # Save the merged dataframe to the specified path
    output_file = f"{output_path}"
    merged_df.to_csv(output_file, index=False, columns=['Game Collection', 'Rank', 'Current Player Count',
                                                        'Peak Player Count', 'Total Hours Spent'])

    print(f"Data saved to '{output_file}'")

    return output_file



