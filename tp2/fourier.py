#!/usr/bin/python3

from cmath import exp, pi
import numpy as np
import math


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

# def fft(x):
#     N = len(x)
#     if N <= 1:
#         return x
#     even = fft(x[0::2])
#     odd = fft(x[1::2])

#     T = [exp(-2j * pi * k/N) * odd[k] for k in range(N//2)]

#     return [even[k] + T[k] for k in range(N//2)] + [even[k] - T[k] for k in range(N//2)]
