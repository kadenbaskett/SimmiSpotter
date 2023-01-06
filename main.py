import pricing_data

amc_ohlc = pricing_data.get_intraday_data('AMC', '5min')
print(amc_ohlc)
