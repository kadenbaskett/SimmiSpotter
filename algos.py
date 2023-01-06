import numpy as np


def smooth_price(price, smoothness):
    box = np.ones(smoothness)/smoothness
    price_smooth = np.convolve(price, box, mode='same')
    return price_smooth
