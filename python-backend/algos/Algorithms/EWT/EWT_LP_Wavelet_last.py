import numpy as np
from algos.Algorithms.EWT.EWT_beta import EWT_beta


def EWT_LP_Wavelet_last(wn, aw, gamma, N):
    ymw = np.zeros(N)

    an = 1 / (2 * gamma * wn)
    pbn = (1 + gamma) * wn
    mbn = (1 - gamma) * wn

    for k in range(N):
        if aw[k] >= pbn:
            ymw[k] = 1
        elif mbn <= aw[k] <= pbn:
            ymw[k] = np.sin(np.pi * EWT_beta(an * (aw[k] - mbn)) / 2)

    return ymw