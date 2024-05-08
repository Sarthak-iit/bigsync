import numpy as np
from algos.Algorithms.OSLP.diff_extrp import diff_extrp
# Assuming `t1`, `dP1`, `dQ1`, `dV1`, `dVa1` are numpy arrays
# Example usage
# ts, sum, sum_r, dPdF, dQdV, dPdV, dQdF, W_total = DEF_line_intA(t1, dP1, dQ1, dV1, dVa1)

def DEF_line_intA(t1, dP1, dQ1, dV1, dVa1, st, ed):
    dP1 = dP1[st:ed, :]
    dQ1 = dQ1[st:ed, :]
    nl = ed - st
    ts = []
    sum_total = []    
    n_rows = len(dP1)
    n_col = len(dP1[0])
    ddV = np.zeros((n_rows, n_col))  # Initialize ddV matrix
    ddVa = np.zeros((n_rows, n_col))  # Initialize ddVa matrix
    dvolt = np.zeros((n_rows, n_col)) 
    dangle = np.zeros((n_rows, n_col)) 
    
    tempp = np.zeros((n_rows, n_col)) 
    tempq = np.zeros((n_rows, n_col)) 
    for j in range(n_col):
        x = diff_extrp(dV1[:,j],st,ed)
        y = diff_extrp(dVa1[:,j],st,ed)
        ddV[:,j] = x
        ddVa[:,j] = y
        ind = 0
        for i in range(st, ed):
            dvolt[ind,j] = ddV[i - st,j] / dV1[i, j]
            dangle[ind,j] = ddVa[i - st,j] / 180 * np.pi
            ind += 1
        nl = len(dP1)
        sump = np.zeros((nl+1, n_col))
        sumq = np.zeros((nl+1, n_col)) 
        for i in range(nl):
            tempp[i,j] =  dP1[i, j] * dangle[i,j] / 180*np.pi
            tempq[i,j] =  dQ1[i, j] * dvolt[i,j]
            sump[i + 1, j] = sump[i, j] + tempp[i,j]
            sumq[i + 1, j] = sumq[i, j] + tempq[i,j]

        sum_total.append((sump[1:, j] + sumq[1:, j]).tolist())
        # dPdF.append(sump[1:, j].tolist())
        # dQdV.append(sumq[1:, j].tolist())
        ts = t1[st:ed]
    return ts, sum_total