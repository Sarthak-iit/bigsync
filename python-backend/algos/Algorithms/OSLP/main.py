import numpy as np
import math
from algos.Algorithms.OSLP.diff_extrp import diff_extrp
from algos.Algorithms.OSLP.def_line_intA import DEF_line_intA
from algos.Algorithms.OSLP.calculatePower import LineFlowCalculation
from algos.Algorithms.OSLP.denoise import denoiseSignal
def removeNan(arr):
    curr = arr[0]
    for i in range(len(arr)):
        if math.isnan(arr[i]) or arr[i] == 0:
            # print("yes")
            arr[i] = curr
        else:
            curr = arr[i]
    return arr

def oslp_main(t, data, st, ed):
    st = int((st-t[0])/(t[1]-t[0]))
    ed = int((ed-t[0])/(t[1]-t[0]))
   
    l = ed-st+1
    m = 0
    for key in data:
        data[key]['VM']= removeNan(data[key]['VM'])
        data[key]['IM']= removeNan(data[key]['IM'])
        data[key]['VA']= removeNan(data[key]['VA'])
        data[key]['IA']= removeNan(data[key]['IA'])
        
    for key in data:
        [P,Q] = LineFlowCalculation(data[key]['VM'], data[key]['VA'], data[key]['IM'], data[key]['IA'])
        if m == 0: m = len(P)
        data[key]['P'] = P
        data[key]['Q'] = Q
    # with open('output.txt', 'w') as f:
    #     for key, value in data.items():
    #         f.write(f"{key}: {value}\n")
    dP = np.zeros((l, len(data.keys())))
    dQ = np.zeros((l, len(data.keys())))
    dV = np.zeros((m, len(data.keys())))
    dVa = np.zeros((m, len(data.keys())))

    index = 0
    for key in data:
        dP[:,index] = data[key]['P'][st:ed+1]
        dQ[:,index] = data[key]['Q'][st:ed+1]
        dV[:,index] = data[key]['VM']
        dVa[:,index] = data[key]['VA']
        index += 1

    fs = 250
    t = np.arange(0, 200, 1/fs)

    
    numSections = len(data.keys())
    ts, sum_ = DEF_line_intA(t, dP, dQ, dV, dVa, st, ed)
    DEF_line = [] 
    Amatrix = np.vstack([ts, np.ones_like(ts)]).T
    for j in range(numSections):
        para = np.linalg.lstsq(Amatrix, sum_[j], rcond=None)[0]
        if math.isnan(para[0]):
            para[0] = 0
        DEF_line.append(para[0])

    # DE ranking
    abs_values = np.abs(DEF_line)
    DEF_Ranking_Line = np.array([np.arange(1, len(DEF_line)+1),DEF_line/max(abs_values)]).T
    DEF_Ranking_Line = DEF_Ranking_Line[np.argsort(abs_values)[::-1]]  
    # np.savetxt('output.txt', DEF_Ranking_Line)
    
    ranking_f = [list(data.keys())[int(i-1)] for i in DEF_Ranking_Line[:, 0][:5]]
    def_ranked = DEF_Ranking_Line[:, 1]
    def_ranked = [f'{val:.2f}' for val in def_ranked]
    print(DEF_Ranking_Line[:,1])
    res = {'rank':ranking_f,'slope':[sum_[int(i-1)] for i in DEF_Ranking_Line[:, 0][:5]], 'def':def_ranked}
    # np.savetxt('output2.txt', [list(data.keys())[int(i-1)] for i in DEF_Ranking_Line[:, 0]])
    with open('output.txt', 'w') as f:
        for i in range(len(DEF_Ranking_Line[:, 0])):
            f.write(f"{list(data.keys())[int(DEF_Ranking_Line[:,0][i])-1]}, {DEF_Ranking_Line[:,1][i]}\n")
    return res