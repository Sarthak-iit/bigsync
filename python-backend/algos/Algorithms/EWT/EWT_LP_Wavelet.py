import numpy as np
from algos.Algorithms.EWT.EWT_beta import EWT_beta

def EWT_LP_Wavelet(wn, wm, aw, gamma, N):
    # Initialize the Fourier transform of the wavelet
    ymw = np.zeros(N)

    if wn > np.pi:
        a = 1
    else:
        a = 0

    an = 1 / (2 * gamma * np.abs(wn - a * 2 * np.pi))
    pbn = wn + gamma * np.abs(wn - a * 2 * np.pi)
    mbn = wn - gamma * np.abs(wn - a * 2 * np.pi)

    if wm > np.pi:
        a = 1
    else:
        a = 0

    am = 1 / (2 * gamma * np.abs(wm - a * 2 * np.pi))
    pbm = wm + gamma * np.abs(wm - a * 2 * np.pi)
    mbm = wm - gamma * np.abs(wm - a * 2 * np.pi)

    for k in range(N):
        if pbn <= aw[k] <= mbm:
            ymw[k] = 1
        elif mbm <= aw[k] <= pbm:
            ymw[k] = np.cos(np.pi * EWT_beta(am * (aw[k] - mbm)) / 2)
        elif mbn <= aw[k] <= pbn:
            ymw[k] = np.sin(np.pi * EWT_beta(an * (aw[k] - mbn)) / 2)

    return ymw

