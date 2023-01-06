import pricing_data
import matplotlib.pyplot as plt

ticker_data = pricing_data.get_intraday_data('AMC', '5min')

plt.figure()
plt.plot(ticker_data['ohlc4'])
plt.xlabel('Date')
plt.legend(['Price ($)'])
plt.show()
