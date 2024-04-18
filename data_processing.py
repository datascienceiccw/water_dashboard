# data_processing.py

import pandas as pd
from dateutil import parser
from get_data import fetch_data_from_api

# Fetch data from API
API_URL = "https://mongodbapi-bw4d.onrender.com"
data = fetch_data_from_api(API_URL)


def preprocess_data(date_format="%d-%b-%Y %H:%M:%S"):
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format=date_format, errors='coerce')
    df.dropna(subset=['timestamp'], inplace=True)
    df['inputflow'] = df['inputflow'].round().astype(int)
    df['outputflow'] = df['outputflow'].round().astype(int)
    df['inputtds'] = df['inputtds'].round().astype(int)
    df['outputtds'] = df['outputtds'].round().astype(int)
    return df

def filter_data(df, from_date, to_date):
    from_date = parser.parse(from_date)
    to_date = parser.parse(to_date)
    return df[(df['timestamp'].dt.date >= from_date.date()) & (df['timestamp'].dt.date <= to_date.date())]
