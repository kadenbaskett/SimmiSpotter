import os
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv('ALPHA_VANTAGE_API')


def getCandles(ticker):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + \
        ticker + '&interval=5min&apikey=' + api_key
    r = requests.get(url)
    data = r.json()

    # convert to custom object
    return data
