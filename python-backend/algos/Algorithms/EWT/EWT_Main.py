from algos.Algorithms.EWT.iEWT1D import iEWT1D
from algos.Algorithms.EWT.EWT1D import EWT1D
from algos.Algorithms.EWT.Hilbpara_EWT import Hilbpara_EWT
import json
import math
import numpy as np
import statsmodels.api as sm

# function to check whether all elements of an array are real or not
def allElementsOfArrayReal(array):
    truthValues = np.isreal(array)
    for i in truthValues:
        if not i: return False
    return True

# user definded parameters
params = {
    'SamplingRate': 60,
    'globtrend': 'none',
    'reg': 'none',
    'detect': 'locmaxmin',
    'N': 10,
    'completion': 0,
    'log': 0
}
def removeNan(arr):
    curr = 60
    for i in range(len(arr)):
        if math.isnan(arr[i]) or arr[i] == 0:
            arr[i] = curr
        else:
            curr = arr[i]
    return arr
def detrend(arr):
    mean = sum(arr)/len(arr)
    for i in range(len(arr)):
        arr[i] = arr[i] - mean
    return arr

# main function to call
def EWTmainFunction(f):
    f = removeNan(f)
    # f = f[0:int(len(f)/4)]
    f = sm.tsa.detrend(np.array(f), 3,0)
    ewt, mfb, boundaries = EWT1D(f, params)
    tot_ener = np.sum([f[i]*f[i] for i in range(len(f))])
    ener_val = [np.sum(ewt[i] * ewt[i]) for i in range(len(ewt))]
    per_ener = (ener_val / tot_ener) * 100
    ewt2 = []
    for i in range(len(per_ener)):
        if per_ener[i] > 3:
            ewt2.append(ewt[i])
    Ts = 1 / 60
    Fs = 60

    num_ewt = len(ewt2)
    Amp = [0]*num_ewt
    Fr = [0]*num_ewt
    Hil = [0]*num_ewt
    for i in range(num_ewt):
        [Amp[i], Fr[i], Hil[i]] = Hilbpara_EWT(ewt2[i], Ts)
        Fr[i] = sorted(Fr[i])[::-1]
    
    Fr = np.array(Fr)
    Amp = np.array(Amp)
    Or_InstFreq = Fr
    Or_InstEner = Amp*Amp
    ewt2 = np.array(ewt2)
    # return json.dumps({'Amp':Amp.tolist(),'InstEner':Or_InstEner.tolist(),'InstFreq':Or_InstFreq.tolist()})
    return {'Amp':Amp,'InstEner':Or_InstEner,'InstFreq':Or_InstFreq,'ewt':ewt2, 'PerEner':per_ener}