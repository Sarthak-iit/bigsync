import numpy as np

def spectrum_analysis(data):
    Fs = 30  
    Fth = 0.08 
    xx = data - np.mean(data, axis=0)
    NFFT = xx.shape[0]
    S = 2 * np.fft.fft(xx,n=NFFT, axis=0) / xx.shape[0]  
    f = Fs / 2 * np.linspace(0, 1, NFFT//2 + 1) 
    m = np.abs(S)  
    a = np.angle(S) * 180 / np.pi  
    ss_sum = np.sum(m, axis=1) 
    ind = np.argsort(np.abs(f - Fth))
    i1 = ind[0]  # index of Fth    
    idx = np.argsort(ss_sum[i1:len(f)])[::-1]
    Fdominant = f[idx[0] + i1]  # dominant frequency    
    return f, ss_sum, Fdominant