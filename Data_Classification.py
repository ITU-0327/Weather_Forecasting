import os
import glob
import pandas as pd
from config import config

download_path = r"C:\Users\itung\Downloads"
path = r"C:\Users\itung\OneDrive\桌面\Data Science Midterm\Weather Data"  # path to directory containing the files

col_to_remove = ["SeaPres", "Td dew point", "WSGust", "WDGust", "PrecpHour", "SunShine", "GloblRad", "Visb", "UVI",
                 "Cloud Amount"]

all_files = glob.glob(os.path.join(download_path, "C0F9T0*.csv"))  # list of all CSV files in directory

dfs = []  # list to store individual dataframes
for file in all_files:
    df = pd.read_csv(file, skiprows=1)  # read the file, skipping the first row
    filename = os.path.basename(file)
    year, month, day = filename.split('-')[1:4]
    day = day.replace('.csv', '')  # extract the year, month, and day from the filename
    df.insert(0, 'Year', year)  # add columns for the year, month, and day
    df.insert(1, 'Month', month)
    df.insert(2, 'Day', day)
    dfs.append(df)  # add the dataframe to the list
    # remove the file when it set to true
    if config['remove_files']:
        os.remove(file)

# group dataframes by month and concatenate into separate dataframes
month_dfs = {}
for df in dfs:
    year = df['Year'].iloc[0]
    month = df['Month'].iloc[0]
    month_key = f"{year}-{month}"
    if month_key not in month_dfs:
        month_dfs[month_key] = [df]
    else:
        month_dfs[month_key].append(df)

# concatenate dataframes within each month into a single dataframe
for month_key, month_df_list in month_dfs.items():
    month_df = pd.concat(month_df_list)
    year_col = month_df.pop('Year')  # remove the Year column
    month_col = month_df.pop('Month')  # remove the Month column
    day_col = month_df.pop('Day')  # remove the Day column
    month_df.insert(0, 'Year', year_col)  # insert the Year column at the front
    month_df.insert(1, 'Month', month_col)
    month_df.insert(2, 'Day', day_col)  # insert the Day column at the third position

    # remove all the empty columns
    for col in col_to_remove:
        month_df.pop(col)

    # write the dataframe to a new CSV file
    filename = f"{year_col.iloc[0]}-{month_col.iloc[0]}-combined.csv"
    month_df.to_csv(os.path.join(path, filename), index=False)
