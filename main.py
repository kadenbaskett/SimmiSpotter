import algos
import pricing_data
import matplotlib.pyplot as plt

ticker_data = pricing_data.get_intraday_data('AMC', '5min')

ticker_data['Smooth'] = algos.smooth_price(ticker_data['ohlc4'], 5)

print('ticker_data: ', ticker_data)

plt.figure()
plt.plot(ticker_data['ohlc4'])
plt.plot(ticker_data['Smooth'])
plt.xlabel('Date')
plt.legend(['Price ($)'])
plt.show()
