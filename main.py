from datetime import datetime
import algos
import pricing
import plotly.graph_objects as go


ticker = 'SPY'
interval = '60min'
startDate = datetime(2021, 11, 1, 0, 0, 0)

# ticker_data = pricing.get_intraday_data(ticker, interval)
ohlc_data = pricing.get_historical_data(ticker, startDate)

# smoothed_curve = algos.lowess_smooth(
#     ohlc_data.index, ohlc_data['ohlc4'], .3)

# ohlc_data['smooth'] = smoothed_curve[::-1]

# plot price
fig = go.Figure(data=[go.Candlestick(x=ohlc_data.index,
                open=ohlc_data['open'],
                high=ohlc_data['high'],
                low=ohlc_data['low'],
                close=ohlc_data['close'],
                increasing_line_color='rgb(4, 59, 92)', decreasing_line_color='rgb(110, 48, 75)'
                )])

fig.update_layout(
    plot_bgcolor='rgba(14,17,17,1)',
    title={
        'text': 'Parabola Analysis',
        'x': 0.5,  # Set the x position to 0.5 for center alignment
        'xanchor': 'center',  # Anchor the x position to the center
        'y': 0.95  # Set the y position for the title
    },    yaxis_title=ticker,
    xaxis_rangeslider_visible=False,
    xaxis=dict(
        showgrid=False  # Remove x-axis grid lines
    ),
    yaxis=dict(
        showgrid=False  # Remove y-axis grid lines
    )
)

fig.show()
