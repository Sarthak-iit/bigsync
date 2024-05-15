import numpy as np
from algos.Algorithms.EWT.EWT_LocalMaxMin_change import EWT_LocalMaxMin_change


def EWT_Boundaries_Detect_ch(f, params):
    if params['log'] == 1:
        f = np.log(f)
    method = params['detect'].lower()
    boundaries = []
    boundaries = EWT_LocalMaxMin_change(f, params['N'])
    return boundaries

