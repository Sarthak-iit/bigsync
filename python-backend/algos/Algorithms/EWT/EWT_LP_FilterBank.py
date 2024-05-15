import numpy as np
from algos.Algorithms.EWT.EWT_LP_Scaling import EWT_LP_Scaling
from algos.Algorithms.EWT.EWT_LP_Wavelet import EWT_LP_Wavelet
from algos.Algorithms.EWT.EWT_LP_Wavelet_last import EWT_LP_Wavelet_last


def EWT_LP_FilterBank(boundaries, N, cpx):
    Npic = len(boundaries)
    gamma = 1

    for k in range(Npic - 1):
        if (boundaries[k] <= np.pi) and (boundaries[k + 1] > np.pi):
            r = min((boundaries[k + 1] - np.pi) / (boundaries[k + 1] + np.pi),
                    (np.pi - boundaries[k]) / (np.pi + boundaries[k]))
        else:
            r = (boundaries[k + 1] - boundaries[k]) / (boundaries[k + 1] + boundaries[k])
            
        if r < gamma:
            gamma = r
    
    if cpx == 0:
        r = (np.pi - boundaries[Npic - 1]) / (np.pi + boundaries[Npic - 1])
    else:
        r = (2 * np.pi - boundaries[Npic - 1]) / (2 * np.pi + boundaries[Npic - 1])
    
    if r < gamma:
        gamma = r
    
    gamma = (1 - 1 / N) * gamma

    
    Mi = N // 2
    w = np.arange(0, 2 * np.pi, 2 * np.pi / N)
    
    if cpx == 0:
        w[Mi:] = -2 * np.pi + w[Mi:]
        w = np.abs(w)
        mfb = [None] * (Npic + 1)
        mfb[0] = EWT_LP_Scaling(boundaries[0], w, gamma, N)

        for k in range(Npic - 1):
            mfb[k + 1] = EWT_LP_Wavelet(boundaries[k], boundaries[k + 1], w, gamma, N)
        
        mfb[Npic] = EWT_LP_Wavelet_last(boundaries[Npic - 1], w, gamma, N)
    # else:
    #     mfb = [None] * (Npic + 1)
    #     mfb[0] = EWT_LP_Scaling_cpx(boundaries[0], boundaries[-1], w, gamma, N)
    #     shift = 0
        
    #     for k in range(Npic - 1):
    #         if (boundaries[k] <= np.pi) and (boundaries[k + 1] > np.pi):
    #             mfb[k + 1 + shift] = EWT_LP_Wavelet_cpx_HFlow(boundaries[k], w, gamma, N)
    #             mfb[k + 2 + shift] = EWT_LP_Wavelet_cpx_HFup(boundaries[k + 1], w, gamma, N)
    #             shift = 1
    #         else:
    #             mfb[k + 1 + shift] = EWT_LP_Wavelet(boundaries[k], boundaries[k + 1], w, gamma, N)
    
    return mfb
