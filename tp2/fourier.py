#!/usr/bin/python3

from cmath import exp, pi
import numpy as np
import math
from scipy import signal


def fft(x):
    N = len(x)
    if N <= 1:
        return x
    oddItems = fft(x[1::2])
    evenItems = fft(x[0::2])
    rangeToUse = range(math.trunc(N / 2))
    auxCalc = -2j * pi
    L = []
    R = []
    for k in rangeToUse:
        T = exp(auxCalc * k / N) * oddItems[k]
        L.append(evenItems[k] + T)
        R.append(evenItems[k] - T)
    return L + R

# Referencing filter from https://scipy.github.io/old-wiki/pages/Cookbook/ButterworthBandpass
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y
