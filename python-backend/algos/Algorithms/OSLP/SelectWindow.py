def SlctTWnd1(t, p_ln, td):
    if td:
        tFrom = td[0]
        tTo = td[1]
    else:
        tFrom = t[0]
        tTo = t[-1]

    tst_ind = next((i for i, val in enumerate(t) if val > tFrom), None)
    if tst_ind and tst_ind > 0:
        tst = tst_ind - 1
    else:
        tst = tst_ind

    ted_ind = next((i for i, val in enumerate(t) if val > tTo), None)
    if ted_ind is None:
        ted = len(t)
    else:
        ted = ted_ind
    t1 = t[tst:ted]
    p_ln_1 = p_ln[tst:ted]

    return t1, p_ln_1