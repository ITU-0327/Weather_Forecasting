import os
import pandas as pd
from config import config


def clean_col_data(data, col_name, method):
    cleaning_method = {
        'bfill': data[col_name].fillna(method='bfill'),
        'ffill': data[col_name].fillna(method='ffill'),
        'mean': data[col_name].fillna(data[col_name].mean()),
        'avg': data[col_name].fillna((data[col_name].ffill() + data[col_name].bfill()) / 2),
        '0': data[col_name].fillna(0),
        'delete': data.dropna(subset=[col_name])
    }
    if method not in cleaning_method.keys():
        print("The method from the config is wrong, using 'bfill' as default.")
        method = 'bfill'

    if method == 'delete':
        data = cleaning_method[method]
    else:
        data[col_name] = cleaning_method[method]
    return data


df = pd.read_csv(os.path.join(config['path'], f'{config["station_id"]}-combined.csv'))
df = df.apply(pd.to_numeric, errors='coerce')

df = clean_col_data(df, 'Precp', config['method'])

df.to_csv(os.path.join(config['path'], 'test_file.csv'), index=False)
