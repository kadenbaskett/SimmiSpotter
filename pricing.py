import os
from dotenv import load_dotenv
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy.stats import linregress

load_dotenv()

apiToken = os.getenv('POLYGON_KEY')
uri = "https://api.polygon.io"

headers = {
    "Authorization": f"Bearer {apiToken}"
}

class RateLimitError(Exception):
    pass

def getCandles(ticker, interval, afterTimestamp, beforeTimestamp, adjusted='true', sort='asc', limit=50000):
    url = uri + f'/v2/aggs/ticker/{ticker}/range/{interval}/minute/{afterTimestamp}/{beforeTimestamp}?adjusted={adjusted}&sort={sort}&limit={limit}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        candles = cleanCandles(response.json()["results"], ticker)
        return candles

    elif response.status_code == 429:
        raise RateLimitError(f"Polygon rate limit exceeded. Unable to fetch data.")
    else:
        raise Exception('Error fetching Polygon data')

def cleanCandles(candleData, ticker):
    for candle in candleData:
        candle.pop('vw', None)
        candle.pop('n', None)
        ohlc4 = (candle["o"] + candle["h"] + candle["l"] + candle["c"]) / 4
        candle["ohlc4"] = ohlc4

    df = pd.DataFrame(candleData)
    df['t'] = pd.to_datetime(df['t'], unit='ms')
    df['day'] = df['t'].dt.date

    day_grouped_data = df.groupby('day')

    # Create subplots
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)

    # Add OHLC4 trace
    fig.add_trace(go.Scatter(x=df.index, y=df['ohlc4'],
                             mode='lines',
                             name='OHLC4',
                             hovertemplate='%{y:.2f}<br>%{text}',
                             text=df['t'].dt.strftime('%Y-%m-%d %H:%M:%S')), row=1, col=1)

    # Add OHLC4 Daily highs trace
    daily_highs = day_grouped_data['ohlc4'].idxmax()

    # Add OHLC4 Daily lows trace
    daily_lows = day_grouped_data['ohlc4'].idxmin()

    # Add OHLC4 midpoints of daily highs and lows trace
    midpoints = (df.loc[daily_highs]['ohlc4'].values + df.loc[daily_lows]['ohlc4'].values) / 2
    midpoint_indices = (daily_highs + daily_lows) // 2

    # Convert to pandas series
    midpoint_indices = pd.Series(midpoint_indices)
    midpoints = pd.Series(midpoints)

    midpoints_trace = go.Scatter(
        x=midpoint_indices.iloc[:].values,
        y=midpoints.iloc[:].values,
        mode='markers',
        marker=dict(color='black', size=8),
        name='Midpoints',
        hovertemplate='Midpoint: %{y:.2f}<br>%{text}',
        text=midpoint_indices.iloc[:].values    
    )
    fig.add_trace(midpoints_trace, row=1, col=1)
    
    # Add curve between midpoint points
    curve_trace = go.Scatter(
        x=midpoint_indices.iloc[:].values,
        y=midpoints.iloc[:].values,
        mode='lines',
        line=dict(color='black'),
        name='Curve'
    )
    fig.add_trace(curve_trace, row=1, col=1)

    # Calculate second derivative of midpoints
    second_derivative = np.gradient(np.gradient(midpoints))
        
    # Calculate 1, 2, and 3 standard deviations levels
    std_dev = np.std(second_derivative)
    std_dev_1 = std_dev
    std_dev_2 = 2 * std_dev
    std_dev_3 = 3 * std_dev

    # Identify points where the second derivative changes aggressively
    std_dev_1_change_points = np.where(np.abs(second_derivative) > std_dev)[0]
    std_dev_1_change_points_trace = go.Scatter(
        x=midpoint_indices.iloc[std_dev_1_change_points].values,
        y=midpoints.iloc[std_dev_1_change_points].values,
        mode='markers',
        marker=dict(color='green', size=8),
        name='Aggressive Changes',
        hovertemplate='Aggressive Change: %{y:.2f}<br>%{text}',
        text=midpoint_indices.iloc[std_dev_1_change_points].values
    )
    fig.add_trace(std_dev_1_change_points_trace, row=1, col=1)

    std_dev_2_change_points = np.where(np.abs(second_derivative) > std_dev_2)[0]
    std_dev_2_change_points_trace = go.Scatter(
        x=midpoint_indices.iloc[std_dev_2_change_points].values,
        y=midpoints.iloc[std_dev_2_change_points].values,
        mode='markers',
        marker=dict(color='blue', size=8),
        name='Aggressive Changes',
        hovertemplate='Aggressive Change: %{y:.2f}<br>%{text}',
        text=midpoint_indices.iloc[std_dev_2_change_points].values
    )
    fig.add_trace(std_dev_2_change_points_trace, row=1, col=1)

    std_dev_3_change_points = np.where(np.abs(second_derivative) > std_dev_3)[0]
    std_dev_3_change_points_trace = go.Scatter(
        x=midpoint_indices.iloc[std_dev_3_change_points].values,
        y=midpoints.iloc[std_dev_3_change_points].values,
        mode='markers',
        marker=dict(color='purple', size=8),
        name='Aggressive Changes',
        hovertemplate='Aggressive Change: %{y:.2f}<br>%{text}',
        text=midpoint_indices.iloc[std_dev_3_change_points].values
    )
    fig.add_trace(std_dev_3_change_points_trace, row=1, col=1)

    # Identify continuous sections with 3 or more midpoints without aggressive change
    sections = []
    current_section = []
    for idx in range(len(midpoint_indices)):
        if idx not in std_dev_1_change_points:
            current_section.append(idx)  # Use idx instead of val
        else:
            if len(current_section) >= 3:
                sections.append(current_section)
            current_section = []

    # Perform linear regression for each identified section
    for section in sections:
        valid_indices = [idx for idx in section if idx < len(midpoint_indices)]
        if len(valid_indices) >= 4:
            first_midpoint_index = valid_indices[0]
            last_midpoint_index = valid_indices[-1]  # Use the last midpoint index in the section
            x_values = midpoint_indices.iloc[range(first_midpoint_index, last_midpoint_index + 1)].values
            y_values = midpoints.iloc[range(first_midpoint_index, last_midpoint_index + 1)].values
            slope, intercept, r_value, p_value, std_err = linregress(x_values, y_values)
            regression_line = slope * x_values + intercept
            regression_trace = go.Scatter(x=x_values, y=regression_line,
                                        mode='lines',
                                        line=dict(color='green', width=4),
                                        name='Linear Regression')
            fig.add_trace(regression_trace, row=1, col=1)

    # Add second derivative subplot
    second_derivative_trace = go.Scatter(x=midpoint_indices, y=second_derivative,
                                        mode='lines',
                                        line=dict(color='black'),
                                        name='Second Derivative')
    fig.add_trace(second_derivative_trace, row=2, col=1)

    # Add 1, 2, and 3 standard deviations levels to second derivaitc plot
    std_dev_1_trace_positive = go.Scatter(x=midpoint_indices, y=np.full_like(midpoints, std_dev_1),
                               mode='lines',
                               line=dict(color='green', dash='dash'),
                               name='1 Std Dev')
    std_dev_1_trace_negative = go.Scatter(x=midpoint_indices, y=np.full_like(midpoints, -std_dev_1),
                               mode='lines',
                               line=dict(color='green', dash='dash'),
                               name='1 Std Dev')
    std_dev_2_trace_positive = go.Scatter(x=midpoint_indices, y=np.full_like(midpoints, std_dev_2),
                               mode='lines',
                               line=dict(color='blue', dash='dash'), 
                               name='2 Std Dev')
    std_dev_2_trace_negative = go.Scatter(x=midpoint_indices, y=np.full_like(midpoints, -std_dev_2),
                               mode='lines',
                               line=dict(color='blue', dash='dash'),
                               name='2 Std Dev')
    std_dev_3_trace_positive = go.Scatter(x=midpoint_indices, y=np.full_like(midpoints, std_dev_3),
                               mode='lines',
                               line=dict(color='purple', dash='dash'),  
                               name='3 Std Dev')
    std_dev_3_trace_negative = go.Scatter(x=midpoint_indices, y=np.full_like(midpoints, -std_dev_3),
                            mode='lines',
                            line=dict(color='purple', dash='dash'),  
                            name='3 Std Dev')

    fig.add_trace(std_dev_1_trace_positive, row=2, col=1)
    fig.add_trace(std_dev_1_trace_negative, row=2, col=1)
    fig.add_trace(std_dev_2_trace_positive, row=2, col=1)
    fig.add_trace(std_dev_2_trace_negative, row=2, col=1)
    fig.add_trace(std_dev_3_trace_positive, row=2, col=1)
    fig.add_trace(std_dev_3_trace_negative, row=2, col=1)

    # Update layout
    fig.update_layout(
                      title=ticker,
                      xaxis_title='Index',
                      hovermode='x')

    fig.show()

    return candleData
