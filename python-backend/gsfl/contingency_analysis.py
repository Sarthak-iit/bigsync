import numpy as np
from gsfl.gsfl_algorithm import perform_gauss_seidel,calculate_Vbus

def calculate_base_flows(bus_data: np.ndarray, line_data : np.ndarray):
    Vbus = calculate_Vbus(line_data,bus_data,1)
    num_lines = line_data.shape[0]
    P_line = np.zeros(num_lines)
    for k in range(num_lines):
        i = int(line_data[k,1])
        j = int(line_data[k,2])
        x_ij = line_data[k,4]
        V_i = np.abs(Vbus[i-1])
        V_j = np.abs(Vbus[j-1])
        Q_i = np.angle(Vbus[i-1])
        Q_j = np.angle(Vbus[j-1])
        P = ((V_i*V_j)/x_ij)*np.sin(Q_i-Q_j)
        P_line[k]=P
    return P_line
        
    
    


def calculate_losf(Ybus: np.ndarray, line_data:np.ndarray , base_flows: np.ndarray, outageLine) -> np.ndarray:
    """
    Calculate Line Outage Sensitivity Factor (LOSF).
    """
    num_lines = base_flows.shape[0]
    LOSF = [
    {"line_no": i + 1, "orig_pline": None, "losf": None, "p_calc": None} 
    for i in range(num_lines)
    ]
    B = np.imag(Ybus[1:,1:])
    B *= -1
    X = np.linalg.inv(B)
    m = int(line_data[int(outageLine)-1,1])-1
    n = int(line_data[int(outageLine)-1,2])-1
    for l in range(num_lines):
        LOSF[l]['orig_pline'] = base_flows[l]
        if l== int(outageLine)-1:
            LOSF[l]['losf'] = 0
            LOSF[l]['p_calc'] = 0
            continue
        p = int(line_data[l,1])-1
        q = int(line_data[l,2])-1
        x_b = line_data[int(outageLine)-1,4]
        x_c = line_data[l,4]
        X_pn = get_X(p,n,X)
        X_pm = get_X(p,m,X)
        X_qn = get_X(q,n,X)
        X_qm = get_X(q,n,X)
        X_mm = get_X(m,m,X)
        X_mn = get_X(m,n,X)
        X_nn = get_X(n,n,X)
        X_Th_mn = X_mm + X_nn - 2 * X_mn
        losf = (x_b/x_c)*(((X_pn-X_pm) - (X_qn-X_qm))/(X_Th_mn-x_b))
        LOSF[l]['losf'] = losf
        p_new = base_flows[l] - losf*base_flows[int(outageLine)-1]
        LOSF[l]['p_calc'] = p_new
    return LOSF

def get_X(p,q,X):
    return X[p-1,q-1] if p>=0 and q>=0 else 0

def calculate_gosf(Ybus: np.ndarray, line_data:np.ndarray , base_flows: np.ndarray, outageGen) -> np.ndarray:
    """
    Calculate Generator Outage Sensitivity Factor (GOSF).
    """
    num_lines = base_flows.shape[0]
    GOSF = [
    {"line_no": i + 1, "orig_pline": None, "gosf": None, "p_calc": None} 
    for i in range(num_lines)
    ]
    B = np.imag(Ybus[1:,1:])
    B *= -1
    X = np.linalg.inv(B)
    k = int(outageGen)-2
    for l in range(num_lines):
        
        GOSF[l]['orig_pline'] = base_flows[l]
        i = int(line_data[l,1])-2
        j = int(line_data[l,2])-2
        x_ij = line_data[l,4]   
        X_ik = X[i,k] if i>=0 else 0
        X_jk = X[j,k] if j>=0 else 0
        gosf = (X_ik - X_jk)/x_ij
        GOSF[l]['gosf'] = gosf
        p_new = base_flows[l] - gosf*line_data[k+1,3]
        GOSF[l]['p_calc'] = p_new
    return GOSF
