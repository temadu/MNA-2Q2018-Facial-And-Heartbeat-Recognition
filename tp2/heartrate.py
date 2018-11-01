# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 19:23:10 2017

@author: pfierens
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2
import fourier as fourier


def analyze(videoPath, isTest):
    cap = cv2.VideoCapture(videoPath)
    # cap = cv2.VideoCapture('toti.mp4')

    # if not cap.isOpened():
    #    print("No lo pude abrir")
    #    return

    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(length)
    print(width)
    print(height)
    print(fps)

    r = np.zeros((1, length))
    g = np.zeros((1, length))
    b = np.zeros((1, length))

    k = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            r[0, k] = np.mean(frame[330:360, 610:640, 0])
            g[0, k] = np.mean(frame[330:360, 610:640, 1])
            b[0, k] = np.mean(frame[330:360, 610:640, 2])
        #        print(k)
        else:
            break
        k = k + 1

    cap.release()
    cv2.destroyAllWindows()

    n = int(np.power(2, np.floor(np.log2(length))))
    f = np.linspace(-n / 2, n / 2 - 1, n) * fps / n

    r = r[0, 0:n] - np.mean(r[0, 0:n])
    g = g[0, 0:n] - np.mean(g[0, 0:n])
    b = b[0, 0:n] - np.mean(b[0, 0:n])
    print(len(r))
    print(len(g))
    print(len(b))

    r = fourier.butter_bandpass_filter(r, 40, 170, fps * 60)
    g = fourier.butter_bandpass_filter(g, 40, 170, fps * 60)
    b = fourier.butter_bandpass_filter(b, 40, 170, fps * 60)


    # np.fft.fft(b))
    R = np.abs(np.fft.fftshift(fourier.fft(r))) ** 2
    G = np.abs(np.fft.fftshift(fourier.fft(g))) ** 2
    B = np.abs(np.fft.fftshift(fourier.fft(b))) ** 2

    if isTest:
        plt.plot(60 * f, R)
        plt.xlim(0, 150)

        plt.plot(60 * f, G)
        plt.xlim(0, 150)
        plt.xlabel("frecuencia [1/minuto]")

        plt.plot(30 * f, B)
        plt.xlim(0, 150)
        plt.show()

    print("Frecuencia cardiaca R: ", abs(f[np.argmax(R)]) * 60, " pulsaciones por minuto")
    print("Frecuencia cardiaca G: ", abs(f[np.argmax(G)]) * 60, " pulsaciones por minuto")
    print("Frecuencia cardiaca B: ", abs(f[np.argmax(B)]) * 60, " pulsaciones por minuto")
