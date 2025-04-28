# gsfl_algorithm.py
import copy
import numpy as np
import pandas as pd
from gsfl.nrlf_algorithm import calculate_line_flows, calculate_power

def calculate_Y_bus(Linlinedata):
    # Number of lines
    Ne = int(np.max(Linlinedata[:, 0]))

    # Number of buses
    Nmax = np.max(Linlinedata[:, 1:3])
    n = int(Nmax)
    
    Ybus = np.zeros((n,n), dtype=complex)
    for p in range(Ne):
        BusP = int(Linlinedata[p,1])-1
        BusQ = int(Linlinedata[p,2])-1
        a=Linlinedata[p,6]; #Tap value for the  p iteration
        if a>0: # for transformers out of nominal position
            yl=(1/((Linlinedata[p,3]+1j*Linlinedata[p,4]))); # line admittance
            Ad=(1j*Linlinedata[p,5]/2); # line charging
            Ybus[BusP,BusQ]=Ybus[BusP,BusQ]-yl/a; # a non diagonal element
            Ybus[BusQ,BusP]=Ybus[BusP,BusQ]; # symmetry is  declared for elements out of the diagonal
            Ybus[BusP,BusP]=Ybus[BusP,BusP]+(yl/a)+((1/a)*(1/a-1)*yl)+Ad; #Equivalent admittance at the P-terminal plus line charging
            Ybus[BusQ,BusQ]=Ybus[BusQ,BusQ]+(yl/a)+(1-1/a)*yl+Ad; #Equivalent admittance at the Q-terminal plus line charging
        else: # for lines
            yl=(1/((Linlinedata[p,3]+1j*Linlinedata[p,4]))); # line admittance
            Ad=(1j*Linlinedata[p,5]/2);  # line charging
            Ybus[BusP,BusQ]=Ybus[BusP,BusQ]-yl; # a non diagonal element
            Ybus[BusQ,BusP]=Ybus[BusP,BusQ]; # symmetry is  declared for elements out of the diagonal
            Ybus[BusP,BusP]=Ybus[BusP,BusP]+yl; # diagonal element
            Ybus[BusQ,BusQ] += yl; # diagonal element
            c=Linlinedata[p,5]; # line charging for the whole line
            if c>0:
                Ybus[BusP,BusP] += Ad; #add value of line charging to the diagonal element
                Ybus[BusQ,BusQ] += Ad; #add value of line charging to the diagonal element
    return Ybus

def calculate_Vbus(linedata, Ndata, acceleration_factor=0):
    # Number of lines
    Ne = int(np.max(linedata[:, 0]))

    # Number of buses
    Nmax = np.max(linedata[:, 1:3])
    n = int(Nmax)
    
    V = np.zeros(n,dtype=complex)
    V += Ndata[:,1]
    Vprev = copy.deepcopy(V)
    
    P = Ndata[:,3] - Ndata[:,5]
    Q = Ndata[:,4] - Ndata[:,6]
    
    Y = calculate_Y_bus(linedata)
    tolerance=1 
    iteration=0
    while (tolerance > 1e-8):
        for k in range(1,n):
            PYV=0
            for i in range(n):
                if k != i:
                    PYV = PYV + Y[k,i]* V[i];  # Vk * Yik
            if Ndata[k,7]==2: # PV bus
                # Estimate Qi at each iteration for the PV buses
                Q[k]=-np.imag(np.conj(V[k])*(PYV + Y[k,k]*V[k]))
            V[k] = (1/Y[k,k])*((P[k]-1j*Q[k])/np.conj(V[k])-PYV) # Compute bus voltages
            if Ndata[k,7] == 2: # For PV buses, the voltage magnitude remains same, but the angle changes
                V[k]=abs(Vprev[k])*(np.cos(np.angle(V[k]))+1j*np.sin(np.angle(V[k])))
        iteration=iteration+1; # Increment iteration count
        tolerance = max(abs(abs(V) - abs(Vprev))); # Tolerance at the current iteration
        Vprev=copy.deepcopy(V)
    return V, iteration, tolerance
    
def perform_gauss_seidel(linedata, busdata, acceleration_factor=0):
    
    Ne = int(np.max(linedata[:, 0]))

    # Number of nodes
    Nmax = np.max(linedata[:, 1:3])
    n = int(Nmax)
    
    Y = calculate_Y_bus(linedata)

    # Iterations
    if n == busdata.shape[0]:
        Vbus,current_iter, error = calculate_Vbus(linedata, busdata, acceleration_factor)

        # Convert Vbus to magnitude and angle
        Vbus_magnitude = np.abs(Vbus)
        Vbus_angle = np.angle(Vbus,deg=True)
        G = np.real(Y)  # Conductance matrix
        B = np.imag(Y)  # Susceptance matrix
        
        P_cal, Q_cal = calculate_power(G, B, Vbus_magnitude, Vbus_angle)
        line_flows = calculate_line_flows(linedata, Vbus)

        # Create a combined list of dictionaries for easier processing
        Vbus_results = [{"magnitude": mag, "angle": angle, "real_power": rp, "complex_power" : cp} for mag, angle,rp,cp in zip(Vbus_magnitude, Vbus_angle,P_cal,Q_cal)]

        return {"final_voltages": Vbus_results,
                "line_flow_results":line_flows,
                "iterations": current_iter,
                "max_mismatch": error}
    
    else:
        return {"error": "Number of buses does not match nodes input"}
