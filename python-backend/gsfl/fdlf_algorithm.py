import numpy as np
from gsfl.nrlf_algorithm import calculate_line_flows, calculate_power


def calculate_Y_bus(Linedata):
    # Number of lines
    Ne = int(np.max(Linedata[:, 0]))

    # Number of buses
    Nmax = np.max(Linedata[:, 1:3])
    n = int(Nmax)
    
    Ybus = np.zeros((n,n), dtype=complex)
    for p in range(Ne):
        BusP = int(Linedata[p,1])-1
        BusQ = int(Linedata[p,2])-1
        a=Linedata[p,6]; #Tap value for the  p iteration
        if a>0: # for transformers out of nominal position
            yl=(1/((Linedata[p,3]+1j*Linedata[p,4]))); # line admittance
            Ad=(1j*Linedata[p,5]/2); # line charging
            Ybus[BusP,BusQ]=Ybus[BusP,BusQ]-yl/a; # a non diagonal element
            Ybus[BusQ,BusP]=Ybus[BusP,BusQ]; # symmetry is  declared for elements out of the diagonal
            Ybus[BusP,BusP]=Ybus[BusP,BusP]+(yl/a)+((1/a)*(1/a-1)*yl)+Ad; #Equivalent admittance at the P-terminal plus line charging
            Ybus[BusQ,BusQ]=Ybus[BusQ,BusQ]+(yl/a)+(1-1/a)*yl+Ad; #Equivalent admittance at the Q-terminal plus line charging
        else: # for lines
            yl=(1/((Linedata[p,3]+1j*Linedata[p,4]))); # line admittance
            Ad=(1j*Linedata[p,5]/2);  # line charging
            Ybus[BusP,BusQ]=Ybus[BusP,BusQ]-yl; # a non diagonal element
            Ybus[BusQ,BusP]=Ybus[BusP,BusQ]; # symmetry is  declared for elements out of the diagonal
            Ybus[BusP,BusP]=Ybus[BusP,BusP]+yl; # diagonal element
            Ybus[BusQ,BusQ] += yl; # diagonal element
            c=Linedata[p,5]; # line charging for the whole line
            if c>0:
                Ybus[BusP,BusP] += Ad; #add value of line charging to the diagonal element
                Ybus[BusQ,BusQ] += Ad; #add value of line charging to the diagonal element
    return Ybus

def perform_fdlf(line_data, bus_data,tolerance=1e-8, max_iteration=1e6):
    n = int(np.max(line_data[:, 1:3]))
    Ybus = calculate_Y_bus(line_data)
    
    V = np.ones(n, dtype=complex) * bus_data[:, 1]
    Psp = (bus_data[:, 3] - bus_data[:, 5])
    Qsp = (bus_data[:, 4] - bus_data[:, 6])
    
    G, B = np.real(Ybus), np.imag(Ybus)
    PV, PQ = np.where(bus_data[:,7] == 2)[0], np.where(bus_data[:,7] == 3)[0]
    NS = np.concatenate((PV, PQ))
    
    B1, B11 = -B[np.ix_(NS, NS)], -B[np.ix_(PQ, PQ)]
    invB1, invB11 = np.linalg.inv(B1), np.linalg.inv(B11)
    
    tol, iteration = 1, 0
    while tol > tolerance and iteration<max_iteration:
        S = V * np.conj(Ybus @ V)
        dP, dQ = np.real(S[NS] - Psp[NS]), np.imag(S[PQ] - Qsp[PQ])
        
        dth = -invB1 @ dP
        dV = -invB11 @ dQ
        
        V[NS] *= np.exp(1j * dth)
        V[PQ] += dV
        
        tol = max(np.abs(np.concatenate((dP, dQ))))
        iteration += 1
    
    Vbus_magnitude, Vbus_angle = np.abs(V), np.angle(V, deg=True)
    line_flows = calculate_line_flows(line_data, V)
    P_cal, Q_cal = calculate_power(G, B, Vbus_magnitude, np.angle(V))
    
    return {"final_voltages": [{"magnitude": mag, "angle": angle, "real_power": rp, "complex_power" : cp} for mag, angle,rp,cp in zip(Vbus_magnitude, Vbus_angle,P_cal,Q_cal)],
            "line_flow_results":line_flows,
            "iterations": iteration,
            "max_mismatch": tol}
