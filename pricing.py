import os
from dotenv import load_dotenv
import requests
import pandas as pd
import plotly.graph_objects as go

load_dotenv()

apiToken = os.getenv('POLYGON_KEY')
uri = "https://api.polygon.io"

headers = {
    "Authorization": f"Bearer {apiToken}"
}

def getCandles(ticker, interval, afterTimestamp, beforeTimestamp, adjusted='true', sort='asc', limit=50000):
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
        ohlc4 = (candle["o"] + candle["h"] + candle["l"] + candle["c"]) / 4
        candle["ohlc4"] = ohlc4

    df = pd.DataFrame(candleData)
    df['t'] = pd.to_datetime(df['t'], unit='ms')
    df['day'] = df['t'].dt.date

    day_grouped_data = df.groupby('day')

    fig = go.Figure()

    # Add OHLC4 trace
    fig.add_trace(go.Scatter(x=df.index, y=df['ohlc4'],
                             mode='lines',
                             name='OHLC4',
                             hovertemplate='%{y:.2f}<br>%{text}',
                             text=df['t'].dt.strftime('%Y-%m-%d %H:%M:%S')))

    # Add highest and lowest points traces
    daily_highs = day_grouped_data['ohlc4'].idxmax()
    daily_lows = day_grouped_data['ohlc4'].idxmin()

    fig.add_trace(go.Scatter(x=daily_highs, y=df.loc[daily_highs]['ohlc4'],
                             mode='markers',
                             marker=dict(color='red', size=8),  # Increase marker size
                             name='Highest Points',
                             hovertemplate='Highest: %{y:.2f}<br>%{text}',
                             text=daily_highs))

    fig.add_trace(go.Scatter(x=daily_lows, y=df.loc[daily_lows]['ohlc4'],
                             mode='markers',
                             marker=dict(color='green', size=8),  # Increase marker size
                             name='Lowest Points',
                             hovertemplate='Lowest: %{y:.2f}<br>%{text}',
                             text=daily_lows))

    # Update layout
    fig.update_layout(title='OHLC4 Data with Highest and Lowest Points',
                      xaxis_title='Index',
                      yaxis_title='OHLC4 Value',
                      hovermode='x')

    # Show the plot
    fig.show()

    return candleData
