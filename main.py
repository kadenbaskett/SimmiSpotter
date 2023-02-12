import algos
import pricing
import matplotlib.pyplot as plt

ticker = 'AMC'
interval = '1min'

ticker_data = pricing.get_intraday_data(ticker, interval)
# ticker_data = pricing.get_historical_data(ticker)

smoothed_curve = algos.lowess_smooth(
    ticker_data.index, ticker_data['ohlc4'], .3)

ticker_data['smooth'] = smoothed_curve[::-1]

# derivate = algos.second_derivative(smoothed_curve)

# print('ticker_data: ', ticker_data)

# plot price and smoothed curve
plt.figure()
plt.plot(ticker_data['ohlc4'])
plt.plot(ticker_data['smooth'])
plt.xlabel('Date')
plt.legend(['Price ($)'])
plt.title(
    label=ticker + ' - ' + interval
)
plt.show()

# plot 2nd derivative of smoothed curve
# plt.figure()
# plt.plot(derivate)
# plt.xlabel('2nd Derivative')
# plt.show()
