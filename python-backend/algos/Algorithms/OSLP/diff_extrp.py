import numpy as np
def diff_extrp(xx, st, ed):
    yy = np.empty(0)

    for i in range(st, ed): 
        T22 = (xx[i + 2] - xx[i - 2]) / 4
        T21 = (xx[i + 1] - xx[i - 1]) / 2
        T11 = T21 + (T22 - T21) / 3
        yy = np.append(yy, T11)
    return yy