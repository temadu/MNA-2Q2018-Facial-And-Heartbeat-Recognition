#!/usr/bin/python3

from cmath import exp, pi

def fft(x):
    N = len(x)
    if N <= 1:
        return x
    even = fft(x[0::2])
    odd = fft(x[1::2])

    T = [exp(-2j * pi * k/N) * odd[k] for k in range(N//2)]

    return [even[k] + T[k] for k in range(N//2)] + [even[k] - T[k] for k in range(N//2)]
