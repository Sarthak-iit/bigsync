import pywt
import numpy as np
def denoiseSignal(sig):
    wavelet = 'db4'
    coeffs = pywt.wavedec(sig, wavelet)
    threshold = np.std(coeffs[-1]) * np.sqrt(2 * np.log(len(sig)))
    new_coeffs = [pywt.threshold(c, threshold, mode='soft') for c in coeffs]
    denoised_signal = pywt.waverec(new_coeffs, wavelet)
    return denoised_signal