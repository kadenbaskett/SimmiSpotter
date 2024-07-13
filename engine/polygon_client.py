import os
from dotenv import load_dotenv
import pandas as pd
import requests

load_dotenv()
apiToken = os.getenv('POLYGON_API_KEY')

uri = "https://api.polygon.io"
headers = {
    "Authorization": f"Bearer {apiToken}"
}
class RateLimitError(Exception):
    pass



def get_agg_candles(ticker, multiplier, timespan, start_date, end_date, adjusted='true', sort='asc', limit=50000):
    ticker = ticker.upper()
    url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{start_date}/{end_date}?adjusted={adjusted}&sort={sort}&limit={limit}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()['results']
            df = pd.DataFrame(data)
            df['time'] = pd.to_datetime(df['t'], unit='ms')

            rename = {'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume', 'time': 'time'}

            ret = df[rename.keys()].rename(columns=rename)
            return ret
        except Exception as e:
            print(f"Error processing data: {e}")
            return None

    elif response.status_code == 429:
        print('Rate limit error')
        raise RateLimitError(f"Polygon rate limit exceeded. Unable to fetch data.")

    else:
        print(f"Error fetching Polygon data: {response.content.decode('utf-8')}")
        return None