import os
import glob
import pandas as pd
from config import config

col_to_remove = ["SeaPres", "Td dew point", "WSGust", "WDGust", "PrecpHour", "SunShine", "GloblRad", "Visb", "UVI",
                 "Cloud Amount"]

all_files = glob.glob(os.path.join(config['download_path'], f"{config['station_id']}*.csv"))

dfs = []
for file in all_files:
    df = pd.read_csv(file, skiprows=1)
    filename = os.path.basename(file)
    year, month, day = filename.split('-')[1:4]
    day = day.replace('.csv', '')
    df.insert(0, 'Year', year)
    df.insert(1, 'Month', month)
    df.insert(2, 'Day', day)
    dfs.append(df)

    if config['remove_files']:
        os.remove(file)

combined_df = pd.concat(dfs)

for col in col_to_remove:
    combined_df.pop(col)

filename = f"{config['station_id']}-combined.csv"
combined_df.to_csv(os.path.join(config['path'], filename), index=False)
