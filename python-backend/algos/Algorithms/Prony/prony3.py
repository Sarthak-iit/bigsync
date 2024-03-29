import numpy as np
from scipy.linalg import toeplitz


def pronyAnalysis(x):
    # x = x.reshape(1, -1)
    # t = t1[chosen_start:chosen_end]
    # Ts = (t[1]-t[0])
    Ts = 0.033
    fs = 1/Ts
    p = 2

    N = len(x)
    T = toeplitz(x[p-1:N - 1], x[p-1::-1])
    xnew = x[p:N]
    # xnew = xnew.reshape(1, -1)
    a = -np.linalg.lstsq(T, xnew.T, rcond=None)[0]
    c = np.concatenate(([1], a))
    r = np.roots(c)
    z = np.log(r) * fs
    wn = abs(z)
    alfa = np.real(z)
    zeta = (alfa / wn) * (-100)
    wd = np.imag(z / (2 * np.pi))

    alfa[np.isinf(alfa)] = np.finfo(float).max * np.sign(alfa[np.isinf(alfa)])
    len_vandermonde = p
    Z = np.zeros((len_vandermonde, p), dtype=complex)
    for i in range(len(r)):
        Z[:, i] = np.transpose(r[i]**np.arange(0, len_vandermonde))

    rz = np.real(Z)
    iz = np.imag(Z)
    rz[np.isinf(rz)] = np.finfo(float).max * np.sign(rz[np.isinf(rz)])
    iz[np.isinf(iz)] = np.finfo(float).max * np.sign(iz[np.isinf(iz)])
    Z = rz + 1j * iz
    xx = x.flatten()[0:len_vandermonde]
    xx = xx.reshape(1, -1)
    h = np.linalg.lstsq(Z, xx.flatten(), rcond=None)[0]

    Amp = abs(h)
    theta = np.arctan2(np.imag(h), np.real(h))
    
    return [wd[0], Amp[0], theta[0], zeta[0]]