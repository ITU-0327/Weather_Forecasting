import os
import pandas as pd
from config import config
import calendar


def clean_col_data(data, col_name):
    cleaning_method = {
        'bfill': data[col_name].fillna(method='bfill'),
        'ffill': data[col_name].fillna(method='ffill'),
        'mean': data[col_name].fillna(data[col_name].mean()),
        'avg': data[col_name].fillna((data[col_name].ffill() + data[col_name].bfill()) / 2),
        'day_mean': data.groupby(['Year', 'Month', 'Day'])[col_name].transform(lambda x: x.fillna(round(x.mean(), 1))),
        'month_mean': data.groupby(['Year', 'Month'])[col_name].transform(lambda x: x.fillna(round(x.mean(), 1))),
        '0': data[col_name].fillna(0),
        'delete': data.dropna(subset=[col_name])
    }
    method = config['method'][col_name]
    if method not in cleaning_method.keys():
        print("The method from the config is wrong, using 'bfill' as default.")
        method = 'bfill'

    if method == 'delete':
        data = cleaning_method[method]
    else:
        data[col_name] = cleaning_method[method]

    # if the method is day_mean, fill the rest with the mean value of the month
    # this will be use when the whole day is empty
    if method == 'day_mean':
        data[col_name] = cleaning_method['month_mean']

    return data


def add_day(data):
    data['Day'] += 1
    max_day = calendar.monthrange(data['Year'], data['Month'])[1]
    if data['Day'] > max_day:
        data['Day'] = 1
        data['Month'] += 1
        if data['Month'] > 12:
            data['Month'] = 1
            data['Year'] += 1
    return data


def convert_time(data):
    if data['ObsTime'] == 24:
        data = add_day(data)
        data['ObsTime'] = 0
    return data


df = pd.read_csv(os.path.join(config['path'], f'{config["station_id"]}-combined.csv'))
df = df.apply(convert_time, axis=1)
df = df.apply(pd.to_numeric, errors='coerce')

df = clean_col_data(df, 'Temperature')
df = clean_col_data(df, 'Precp')
df = clean_col_data(df, 'RH')

df.to_csv(os.path.join(config['path'], 'test_file.csv'), index=False)
