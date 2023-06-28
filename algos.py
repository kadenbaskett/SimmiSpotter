# import numpy as np
# import statsmodels.api as sm


# def smooth_price(price, smoothness):
#     box = np.ones(smoothness)/smoothness
#     smooth_price = np.convolve(price, box, mode='same')
#     return smooth_price


# def lowess_smooth(price, date, smoothness):
#     # Fit the lowess curve to the data
#     lowess = sm.nonparametric.lowess
#     curve = lowess(price, date, smoothness, is_sorted=False)
#     print('Raw Curve: ', curve)

#     # Extract the fitted values from the lowess object
#     smooth_price = curve[:, 0]
#     print('Smoothed price curve: ', smooth_price)
#     return smooth_price


# def second_derivative(curve):
#     return curve.derivative(n=2)
