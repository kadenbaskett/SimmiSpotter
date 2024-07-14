import math
from lightweight_charts import Chart
import numpy as np
import pandas as pd
from polygon_client import get_agg_candles

def apply_gravity(trigger_price, curr_price, gravity):
    gravity_percent = gravity / 100
    price_diff = trigger_price - curr_price
    gravity_effect = price_diff * gravity_percent
    new_trigger = trigger_price - gravity_effect
    return new_trigger

def trigger(data, gravity):
    triggers = pd.DataFrame(columns=['time', '1', '5', 'H', 'D'])
    triggers['time'] = data['time']

    for i in range(len(data)):
        curr_price = data.loc[i, 'close']
        
        # Update '1' trigger every minute
        if i == 0 or math.isnan(triggers.loc[i - 1, '1']):
            triggers.loc[i, '1'] = curr_price  # Initialize to current price if NaN or first trigger value
        else:
            triggers.loc[i, '1'] = apply_gravity(triggers.loc[i - 1, '1'], curr_price, gravity)

        # Update '5' trigger every 5 minutes
        if data.loc[i, 'time'].minute % 5 == 0:
            if i == 0 or math.isnan(triggers.loc[i - 1, '5']):
                triggers.loc[i, '5'] = curr_price  # Initialize to current price if NaN or first trigger value
            else:
                triggers.loc[i, '5'] = apply_gravity(triggers.loc[i - 1, '5'], curr_price, gravity)
        else:
            triggers.loc[i, '5'] = triggers.loc[i - 1, '5'] if i > 0 else pd.NA

        # Update 'H' trigger every hour
        if data.loc[i, 'time'].hour != (data.loc[i - 1, 'time'].hour if i > 0 else None):
            if i == 0 or math.isnan(triggers.loc[i - 1, 'H']):
                triggers.loc[i, 'H'] = curr_price  # Initialize to current price if NaN or first trigger value
            else:
                triggers.loc[i, 'H'] = apply_gravity(triggers.loc[i - 1, 'H'], curr_price, gravity)
        else:
            triggers.loc[i, 'H'] = triggers.loc[i - 1, 'H'] if i > 0 else pd.NA

        # Update 'D' trigger every day
        if data.loc[i, 'time'].date() != (data.loc[i - 1, 'time'].date() if i > 0 else None):
            if i == 0 or math.isnan(triggers.loc[i - 1, 'D']):
                triggers.loc[i, 'D'] = curr_price  # Initialize to current price if NaN or first trigger value
            else:
                triggers.loc[i, 'D'] = apply_gravity(triggers.loc[i - 1, 'D'], curr_price, gravity)
        else:
            triggers.loc[i, 'D'] = triggers.loc[i - 1, 'D'] if i > 0 else pd.NA
        
    return triggers

def identify_inflection_points(triggers, column_name):
    inflection_points = []
    for i in range(1, len(triggers) - 1):
        if (triggers[column_name][i - 1] < triggers[column_name][i] > triggers[column_name][i + 1]) or \
           (triggers[column_name][i - 1] > triggers[column_name][i] < triggers[column_name][i + 1]):
            inflection_points.append(i)
    return inflection_points

def find_midpoints(triggers, inflection_points, column_name):
    midpoints = []
    for i in range(1, len(inflection_points)):
        prev_idx = inflection_points[i - 1]
        curr_idx = inflection_points[i]
        midpoint_idx = (prev_idx + curr_idx) // 2
        midpoint_time = triggers.loc[midpoint_idx, 'time']
        midpoint_value = triggers.loc[midpoint_idx, column_name]
        midpoints.append((midpoint_time, midpoint_value))
    return midpoints

if __name__ == '__main__':
    # end_date = pd.Timestamp.now('UTC').normalize()
    # end_date_unix_ms = int(end_date.timestamp() * 1000)

    # # Calculate start_date (4 business days ago) in Unix timestamp (milliseconds)
    # start_date = pd.bdate_range(end=end_date, periods=2)[0]
    # start_date_unix_ms = int(start_date.timestamp() * 1000)

    ticker = 'TSLA'
    price_data = get_agg_candles(ticker=ticker, multiplier=1, timespan='minute', start_date='2024-04-02', end_date='2024-04-06')
    triggers = trigger(price_data, 7.7)

    chart = Chart(title=ticker, toolbox=True)
    chart.watermark('SimmiSpotter', font_size=32, color='rgba(180, 180, 240, 0.2)')
    # chart.legend(visible=True, font_size=14)
    chart.set(price_data)
    chart.candle_style(up_color='rgba(240, 240, 240, 0.2)',
        down_color='rgba(240, 240, 240, 0.2)',
        border_up_color='rgba(240, 240, 240, 0.2)',
        border_down_color='rgba(240, 240, 240, 0.2)',
        wick_up_color='rgba(240, 240, 240, 0.2)',
        wick_down_color='rgba(240, 240, 240, 0.2)')

    
    # one_trigger = chart.create_line(name='1', color='#7DF9FF', width=3, price_label=True, price_line=False)
    one_trigger = chart.create_line(name='1', color='white', width=2, price_label=True, price_line=False)
    five_trigger = chart.create_line(name='5', color='#FFA500', width=3, price_label=True, price_line=False)
    # hour_trigger = chart.create_line(name='H', color='#9B30FF', width=3, price_label=True, price_line=False)
    # day_trigger = chart.create_line(name='D', color='#FF69B4', width=3, price_label=True, price_line=False)
    
    # one_trigger.set(triggers.dropna(subset=['1']))
    # five_trigger.set(triggers.dropna(subset=['5']))
    # hour_trigger.set(triggers.dropna(subset=['H']))
    # day_trigger.set(triggers.dropna(subset=['D']))

    inflection_points = identify_inflection_points(triggers, '1')
    midpoints = find_midpoints(triggers, inflection_points, '1')

    midpoint_data = pd.DataFrame(midpoints, columns=['time', 'midpoint'])

    for idx, row in midpoint_data.iterrows():
        single_midpoint_data = pd.DataFrame([row])
        line_name = f'midpoint_{idx}'

        curr_time = midpoint_data.loc[idx, 'time']
        curr_time_idx = price_data[price_data['time'] == curr_time].index[0]

        prev_idx = curr_time_idx - 1 if curr_time_idx > 0 else 0
        next_idx = curr_time_idx + 1 if curr_time_idx < len(price_data) - 1 else len(price_data) - 1

        prev_time = price_data.loc[prev_idx, 'time']
        next_time = price_data.loc[next_idx, 'time']

        single_midpoint_data = pd.concat([pd.DataFrame([[prev_time, row['midpoint']]], columns=['time', 'midpoint']), single_midpoint_data])
        single_midpoint_data = pd.concat([single_midpoint_data, pd.DataFrame([[next_time, row['midpoint']]], columns=['time', 'midpoint'])])

        single_midpoint_data.rename(columns={'midpoint': line_name}, inplace=True)

        test = chart.create_line(name=line_name, color='#7DF9FF', width=4, price_label=False, price_line=False)
        test.set(single_midpoint_data)

    chart.show(block=True)