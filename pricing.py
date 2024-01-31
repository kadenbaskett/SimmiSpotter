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

    # # Add OHLC4 trace
    fig.add_trace(go.Scatter(x=df.index, y=df['ohlc4'],
                             mode='lines',
                             name='OHLC4',
                             hovertemplate='%{y:.2f}<br>%{text}',
                             text=df['t'].dt.strftime('%Y-%m-%d %H:%M:%S')))

    # # Add OHLC4 Daily highs trace
    daily_highs = day_grouped_data['ohlc4'].idxmax()
    # fig.add_trace(go.Scatter(x=daily_highs, y=df.loc[daily_highs]['ohlc4'],
    #                          mode='markers',
    #                          marker=dict(color='red', size=8),
    #                          name='Highest Points',
    #                          hovertemplate='Highest: %{y:.2f}<br>%{text}',
    #                          text=daily_highs))

    # Add OHLC4 Daily lows trace
    daily_lows = day_grouped_data['ohlc4'].idxmin()
    # fig.add_trace(go.Scatter(x=daily_lows, y=df.loc[daily_lows]['ohlc4'],
    #                          mode='markers',
    #                          marker=dict(color='green', size=8),
    #                          name='Lowest Points',
    #                          hovertemplate='Lowest: %{y:.2f}<br>%{text}',
    #                          text=daily_lows))

    # Add OHLC4 midpoints of daily highs and lows trace
    midpoints = (df.loc[daily_highs]['ohlc4'].values + df.loc[daily_lows]['ohlc4'].values) / 2
    midpoint_indices = (daily_highs + daily_lows) // 2
    midpoints_trace = go.Scatter(x=midpoint_indices, y=midpoints,
                                mode='markers',
                                marker=dict(color='blue', size=8),
                                name='Midpoints',
                                hovertemplate='Midpoint: %{y:.2f}<br>%{text}',
                                text=midpoint_indices)
    fig.add_trace(midpoints_trace)

    # Add curve between midpoint points
    curve_trace = go.Scatter(x=midpoint_indices, y=midpoints,
                            mode='lines',
                            line=dict(color='purple'),
                            name='Curve')
    fig.add_trace(curve_trace)

    # Update layout
    fig.update_layout(
                      title='OHLC4 Data with Highest, Lowest, and Midpoints',
                      xaxis_title='Index',
                      yaxis_title='OHLC4 Value',
                      hovermode='x')

    fig.show()

    return candleData