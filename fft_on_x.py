import numpy as np

"""
Sample Math File for LaptagBernstein
-------------------------------------
"""

def analyze(arrays):
    #getting the arrays given
    arrayX = arrays[0]
    arrayY = arrays[1]

    #doing some math
    ny = np.abs(np.fft.fft(arrayX))
    freq = np.fft.fftfreq(ny.size)
    idx = np.argsort(freq)

    #returning an array of arrays
    return [freq[idx], ny[idx]]
