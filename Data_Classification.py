import os
import glob
import pandas as pd
from config import config

col_to_remove = ["SeaPres", "Td dew point", "WSGust", "WDGust", "PrecpHour", "SunShine", "GloblRad", "Visb", "UVI",
                 "Cloud Amount"]

# list of all CSV files in directory
all_files = glob.glob(os.path.join(config['download_path'], f"{config['station_id']}*.csv"))

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

# concatenate all dataframes into a single dataframe
combined_df = pd.concat(dfs)

# remove all the empty columns
for col in col_to_remove:
    combined_df.pop(col)

# save the dataframe to a new CSV file
filename = f"{config['station_id']}-combined.csv"
combined_df.to_csv(os.path.join(config['path'], filename), index=False)
