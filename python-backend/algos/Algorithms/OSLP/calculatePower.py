import math
import numpy as np

def LineFlowCalculation(vm, va, im, ia):
    ia = np.unwrap(ia)
    va = np.unwrap(va)
    U = vm * np.exp(1j * va / 180 * np.pi) * 1000
    I = im * np.exp(1j * ia / 180 * np.pi)
    S = U * np.conj(I) * 3
    P = np.real(S)
    Q = np.imag(S)
    return P, Q