import json
import os
from dotenv import load_dotenv
import requests
import pandas as pd

load_dotenv()

apiToken = os.getenv('POLYGON_KEY')
uri = "https://api.polygon.io"

headers = {
    "Authorization": f"Bearer {apiToken}"
}

# ticker = stock cusip
# interval = minute multiplier
# afterTimestamp = millisecond timestamp to get data after
# beforeTimestamp = millisecond timestamp to get data before
def getMinuteCandles(ticker, interval, afterTimestamp, beforeTimestamp, adjusted = 'true', sort = 'asc', limit = 5000):
    url = uri + f'/v2/aggs/ticker/{ticker}/range/{interval}/minute/{afterTimestamp}/{beforeTimestamp}?adjusted={adjusted}&sort={sort}&limit={limit}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Request failed with status code:", response.status_code)