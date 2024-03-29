import numpy as np
def iEWT1D(ewt, mfb, cpx):
    # Perform the Inverse Empirical Wavelet Transform of ewt accordingly to
    # the filter bank mfb

    # We perform the adjoint operator to get the reconstruction
    rec = np.zeros(len(ewt[0]))

    for k in range(len(ewt)):
        if cpx == 0:
            rec = rec + np.real(np.fft.ifft(np.fft.fft(ewt[k]) * mfb[k]))
        else:
            rec = rec + np.fft.ifft(np.fft.fft(ewt[k]) * mfb[k])
    return rec
