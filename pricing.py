import json
import os
from dotenv import load_dotenv
import requests
import pandas as pd

load_dotenv()
api_key = os.getenv('ALPHA_VANTAGE_KEY')


def get_intraday_data(symbol, interval):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={api_key}'
    raw_df = requests.get(url).json()
    df = pd.DataFrame(raw_df[f'Time Series ({interval})']).T
    df = df.rename(columns={'1. open': 'open', '2. high': 'high',
                   '3. low': 'low', '4. close': 'close', '5. volume': 'volume'})
    for i in df.columns:
        df[i] = df[i].astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.iloc[::-1]

    # add OHLC4 column
    df['ohlc4'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4

    return df


def get_historical_data(symbol, start_date=None):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}&outputsize=full'
    raw_df = requests.get(url).json()
    df = pd.DataFrame(raw_df[f'Time Series (Daily)']).T
    df = df.rename(columns={'1. open': 'open', '2. high': 'high', '3. low': 'low',
                   '4. close': 'close', '5. adjusted close': 'adj close', '6. volume': 'volume'})
    for i in df.columns:
        df[i] = df[i].astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.iloc[::-1].drop(['7. dividend amount',
                            '8. split coefficient'], axis=1)
    if start_date:
        df = df[df.index >= start_date]

     # add OHLC4 column
    df['ohlc4'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4

    return df
