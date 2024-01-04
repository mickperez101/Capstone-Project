from sqlite3 import connect

# Creates a Cursor for the Database
conn = connect(r'/Capstone-DataAnalytics/Database/SQLite/ScrappingSites.db')
cur = conn.cursor()

# Data Table Names
library = 'SteamChart'
review = 'BackLogs_Reviews'
stat = 'Overall_Statistics'


# Function to Check if Table Exists
def table_exists(cur, table_name):
    cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return cur.fetchone() is not None


# Function to Create a Table for SteamChart Records
def create_steam_chart_table(cur, table_name):
    if not table_exists(cur, table_name):
        sql_table = f"""
        CREATE TABLE {table_name} (
            ID INTEGER,
            Title TEXT,
            Rank INTEGER,
            Current Players INTEGER,
            Peak Players INTEGER,
            Hours Played INTEGER,
            PRIMARY KEY(ID),
            UNIQUE(Rank)
        )"""

        cur.execute(sql_table)
        print(f"Table '{table_name}' Created.")
    else:
        print(f"Table '{table_name}' already exists.")


# Function to Create a Table for Review Catalog
def create_review_table(cur, table_name):
    if not table_exists(cur, table_name):
        review_table = f"""
        CREATE TABLE {table_name} (
            User_Profile TEXT,
            Title TEXT,
            User_Comment TEXT,
            Star_Rating INTEGER,
            Status TEXT,
            PRIMARY KEY(User_Profile)
        )"""

        cur.execute(review_table)
        print(f"Table '{table_name}' Created.")
    else:
        print(f"Table '{table_name}' already exists.")


# Function to Create a Table for Game Statistics
def create_statistics_table(cur, table_name):
    if not table_exists(cur, table_name):
        statistic_table = f"""
        CREATE TABLE {table_name} (
            Game_ID INTEGER,
            Game_Title VARCHAR,
            Average_Star_Rating DECIMAL(3,2),
            Total_Percent DECIMAL(4,2),
            Completed_Percentage DECIMAL(4,2),
            Shelved_Percentage DECIMAL(4,2),
            PRIMARY KEY(Game_ID)
        )"""

        cur.execute(statistic_table)
        print(f"Table '{table_name}' Created.")
    else:
        print(f"Table '{table_name}' already exists.")


"""

# Create tables
create_steam_chart_table(cur, library)
create_review_table(cur, review)
create_statistics_table(cur, stat)

# Close the connection after all operations
conn.commit()
conn.close()

"""
