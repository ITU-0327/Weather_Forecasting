import os
import glob
import pandas as pd
from config import config


def clean_col_data(data, col_name, method):
    switcher = {
        'bfill': data[col_name].fillna(method='bfill'),
        'ffill': data[col_name].fillna(method='ffill'),
        'mean': data[col_name].fillna(data[col_name].mean()),
        'avg': data[col_name].fillna((data[col_name].ffill() + data[col_name].bfill()) / 2),
        '0': data[col_name].fillna(0)
    }
    if method not in switcher.keys():
        print("The method from the config is wrong, using 'bfill' as default.")
        return data[col_name].fillna(method='bfill')
    return switcher[method]


path = r"C:\Users\itung\OneDrive\桌面\Data Science Midterm\Weather Data"

all_files = glob.glob(os.path.join(path, "2011-12-combined.csv"))

for file in all_files:
    df = pd.read_csv(file)
    # clean_col_data('Precp', config['method'], df)

    df = df.apply(pd.to_numeric, errors='coerce')
    df['Precp'] = clean_col_data(df, 'Precp', config['method'])

    df.to_csv(path + r'\test_file.csv', index=False)
