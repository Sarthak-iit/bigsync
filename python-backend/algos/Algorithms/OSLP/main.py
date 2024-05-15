import numpy as np
import math
from algos.Algorithms.OSLP.def_line_intA import DEF_line_intA
from algos.Algorithms.OSLP.calculatePower import LineFlowCalculation
from algos.Algorithms.OSLP.SelectWindow import SlctTWnd1
from algos.Algorithms.OSLP.spectrumAnalysis import spectrum_analysis
from algos.Algorithms.OSLP.BandPassFilter import BandPassFilter
def removeNan(arr):
    if not math.isnan(arr[0]):
        curr = arr[0]
    else:
        curr = 0
    for i in range(len(arr)):
        if math.isnan(arr[i]) or arr[i] == 0:
            arr[i] = curr
        else:
            curr = arr[i]
    return arr

def oslp_main(t, data, st, ed):
    # st = int((st-t[0])/(t[1]-t[0]))
    # ed = int((ed-t[0])/(t[1]-t[0]))
    st = 40
    ed = 50
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
    
    # making matrices
    P_matrix = []
    Q_matrix = []
    VM_matrix = []
    VA_matrix = []
    for key in data:
        P_matrix.append(data[key]['P'])
        Q_matrix.append(data[key]['Q'])
        VM_matrix.append(data[key]['VM'])
        VA_matrix.append(data[key]['VA'])
    P_matrix = (np.vstack(P_matrix)).T
    Q_matrix = (np.vstack(Q_matrix)).T
    VM_matrix = (np.vstack(VM_matrix)).T
    VA_matrix = (np.vstack(VA_matrix)).T
    x12 = 30
    x14 = 0.05
    x13 = 0.5
    ff, ss, Fdominant1 = spectrum_analysis(P_matrix)
    P1 = BandPassFilter(P_matrix.T, Fdominant1, x14, x12)
    Q1 = BandPassFilter(Q_matrix.T, Fdominant1, x14, x12)
    # V1 = BandPassFilter(VM_matrix.T, Fdominant1, x14, x12)
    # VA1 = BandPassFilter(VA_matrix.T, Fdominant1, x14, x12)
    V1 = VM_matrix
    VA1 = VA_matrix

    td = [st, ed]
    td1 = [td[0] + np.floor((td[1] - td[0]) * (1 - x13) / 2), td[0] + np.floor((td[1] - td[0]) * (1 + x13) / 2)]
    # # Cut period per td1
    DE_t, P2 = SlctTWnd1(t, P1, td1)
    _, Q2 = SlctTWnd1(t, Q1, td1)
    _, V2 = SlctTWnd1(t, V1, td1)
    _, VA2 = SlctTWnd1(t, VA1, td1)
    
    # fs = 250
    # t = np.arange(0, 200, 1/fs)
    numSections = len(data.keys())
    ts, sum_ = DEF_line_intA(t, P2, Q2, V2, VA2, 2, len(DE_t)-3)
    DEF_line = [] 
    Amatrix = np.vstack([ts, np.ones_like(ts)]).T
    for j in range(numSections):
        para = np.linalg.lstsq(Amatrix, sum_[j], rcond=None)[0]
        if math.isnan(para[0]):
            para[0] = 0
        DEF_line.append(para[0])
    for i in range(len(DEF_line)):
        if math.isnan(DEF_line[i]):
            DEF_line[i] = 0
    # DE ranking
    abs_values = np.abs(DEF_line)
    DEF_Ranking_Line = np.array([np.arange(1, len(DEF_line)+1),DEF_line/max(abs_values)]).T
    
    DEF_Ranking_Line = DEF_Ranking_Line[np.argsort(abs_values)[::-1]]  
    
    ranking_f = [list(data.keys())[int(i-1)] for i in DEF_Ranking_Line[:, 0][:5]]
    def_ranked = DEF_Ranking_Line[:, 1]
    def_ranked = [f'{val:.2f}' for val in def_ranked]
   
    res = {'rank':ranking_f,'slope':[sum_[int(i-1)] for i in DEF_Ranking_Line[:, 0][:5]], 'def':def_ranked}
    
    return res