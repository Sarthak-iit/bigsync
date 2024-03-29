from scipy.signal import hilbert
import numpy as np

def Hilbpara_EWT(EWT_Comp, Ts):
    Hil = hilbert(EWT_Comp)
    Amp = np.abs(Hil)
    R = np.real(Hil)
    Im = np.imag(Hil)
    Ph = np.arctan2(Im, R)
    U_Ph = np.unwrap(Ph)
    Fr = np.diff(U_Ph) / Ts / (2 * np.pi)
    return [Amp, Fr, Hil]