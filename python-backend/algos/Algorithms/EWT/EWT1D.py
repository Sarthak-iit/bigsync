import numpy as np
from algos.Algorithms.EWT.EWT_Boundaries_Detect_ch import EWT_Boundaries_Detect_ch
from algos.Algorithms.EWT.EWT_LP_FilterBank import EWT_LP_FilterBank

def EWT1D(f, params):
    ff = np.fft.fft(f)
    if np.isrealobj(f):
        boundaries = EWT_Boundaries_Detect_ch(np.abs(ff[:round(len(ff)/2)]), params)
        boundaries = boundaries * np.pi / round(len(ff)/2)
    else:
        boundaries = EWT_Boundaries_Detect_ch(np.abs(ff), params)
        boundaries = boundaries * 2 * np.pi / len(ff)
        Nb = len(boundaries)
        n = 0
        while n < Nb:
            if np.abs(boundaries[n] - np.pi) < 10 * np.pi / len(f):
                boundaries = np.concatenate((boundaries[:n], boundaries[n+1:]))
                n -= 1
                Nb -= 1
            n += 1
        
    # Build the filter bank
    mfb = EWT_LP_FilterBank(boundaries, len(ff), not np.isrealobj(f))
    
    # Extract subbands by filtering the signal
    ewt = [None] * len(mfb)
    if np.isrealobj(f):
        for k in range(len(mfb)):
            ewt[k] = np.real(np.fft.ifft(np.conj(mfb[k]) * ff))
    else:
        for k in range(len(mfb)):
            ewt[k] = np.fft.ifft(np.conj(mfb[k]) * ff)
    return ewt, mfb, boundaries