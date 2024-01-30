import os
from dotenv import load_dotenv
import requests
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go

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
def getCandles(ticker, interval, afterTimestamp, beforeTimestamp, adjusted = 'true', sort = 'asc', limit = 50000):
    url = uri + f'/v2/aggs/ticker/{ticker}/range/{interval}/minute/{afterTimestamp}/{beforeTimestamp}?adjusted={adjusted}&sort={sort}&limit={limit}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        candles = cleanCandles(response.json()["results"])
        return candles
    
    elif response.status_code == 429:
        print('failed because of rate limiting!!!!!! ):')
    
    else:
        print("Request failed with status code:", response.status_code)
        print("Error message:", response.reason)

    
def cleanCandles(candleData):
    for candle in candleData:
        candle.pop('vw', None) 
        candle.pop('n', None) 
        ohlc4 = (candle["o"] + candle["h"] + candle["l"] + candle["c"]) /4 
        candle["ohlc4"] = ohlc4

    df = pd.DataFrame(candleData)
    df['t'] = pd.to_datetime(df['t'], unit='ms')

    # Plot OHLC4
    fig = go.Figure()

    # Add OHLC4 trace
    fig.add_trace(go.Scatter(x=df.index, y=df['ohlc4'],
                             mode='lines',
                             name='OHLC4',
                             hovertemplate='%{y:.2f}<br>%{text}',
                             text=df['t'].dt.strftime('%Y-%m-%d %H:%M:%S')))

    # Update layout
    fig.update_layout(title='OHLC4 Data',
                      xaxis_title='Timestamp',
                      yaxis_title='OHLC4 Value',
                      hovermode='x')

    # Show the plot
    fig.show()
    
    # plt.plot(df.index, df['ohlc4'], linestyle='-', color='#8F00FF', label='OHLC4')

    # plt.title('OHLC4 Data')
    # plt.xlabel('Timestamp')
    # plt.ylabel('OHLC4 Value')
    # plt.legend()
    # plt.show()

    return candleData