# gsfl_algorithm.py
import copy
import numpy as np
import pandas as pd

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

def calculate_Vbus(Edata, Ndata, acceleration_factor=0):
    # Number of lines
    Ne = int(np.max(Edata[:, 0]))

    # Number of buses
    Nmax = np.max(Edata[:, 1:3])
    n = int(Nmax)
    
    V = np.zeros(n,dtype=complex)
    V += Ndata[:,1]
    Vprev = copy.deepcopy(V)
    
    P = Ndata[:,3] - Ndata[:,5]
    Q = Ndata[:,4] - Ndata[:,6]
    
    Y = calculate_Y_bus(Edata)
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
    return V
    
def perform_gauss_seidel(Edata, Ndata, acceleration_factor=0):
    
    Ne = int(np.max(Edata[:, 0]))

    # Number of nodes
    Nmax = np.max(Edata[:, 1:3])
    n = int(Nmax)
    
    Ybus = calculate_Y_bus(Edata)

    # Iterations
    if n == Ndata.shape[0]:
        Vbus = calculate_Vbus(Edata, Ndata, acceleration_factor)

        # Convert Vbus to magnitude and angle
        Vbus_magnitude = np.abs(Vbus)
        Vbus_angle = np.angle(Vbus,deg=True)

        # Create a combined list of dictionaries for easier processing
        Vbus_results = [{"magnitude": mag, "angle": angle} for mag, angle in zip(Vbus_magnitude, Vbus_angle)]

        return {"final_voltages": Vbus_results}
    else:
        return {"error": "Number of buses does not match nodes input"}

# def calculate_Vbus(Ndata, n, Ybus, acceleration_factor):
#     Zbus = np.linalg.inv(Ybus)

#     # Voltage and power calculations
#     error = np.ones((n, 3), dtype=float)
#     e_ind = np.ones(3 * n, dtype=float)
#     e = 1
#     Pdelta = Ndata[:, 3] - Ndata[:, 5]
#     Qdelta = Ndata[:, 4] - Ndata[:, 6]
#     Vbus = Ndata[:, 1] * np.exp(1j * Ndata[:, 2])
#     Qgen = Ndata[:, 4]
#     Qdel = Ndata[:, 6]

#     # Qmax and Qmin limits
#     Qmax = np.nan_to_num(Ndata[:, 8], nan=np.inf)
#     Qmin = np.nan_to_num(Ndata[:, 9], nan=-np.inf)

#     a = float(acceleration_factor)
#     while e != 0:
#         for L in range(n):
#             for c in range(3):
#                 if error[L, c] < 1e-5:
#                     e_ind[c * n + L] = 0
#         for t in range(n):
#             if Ndata[t, 7] == 1:  # Slack bus
#                 error[t, :] = [0, 0, 0]
#             elif Ndata[t, 7] == 2:  # Load bus
#                 YVsum = sum(Ybus[t, k] * abs(Vbus[k]) for k in range(n)) - Ybus[t, t] * abs(Vbus[t])
#                 Vbus_old = Vbus[t]
#                 Vbus[t] = ((Pdelta[t] - 1j * Qdelta[t]) / abs(Vbus[t]) + YVsum) / Ybus[t, t]
#                 error[t, :] = [abs(Vbus[t]) - abs(Vbus_old), 0, 0]
#             elif Ndata[t, 7] == 3:  # PV bus
#                 YVsum = sum(Ybus[t, k] * abs(Vbus[k]) for k in range(n))
#                 Qdelta_old = Qdelta[t]
#                 Qdelta[t] = -np.imag(np.conj(Vbus[t]) * YVsum)
#                 Qgen[t] = Qdelta[t] + Qdel[t]
#                 if Qgen[t] > Qmax[t]:
#                     Qdelta[t] = Qmax[t] - Qdel[t]
#                     YVsum -= Ybus[t, t] * abs(Vbus[t])
#                     Vbus_old = Vbus[t]
#                     Vbus[t] = ((Pdelta[t] - 1j * Qdelta[t]) / abs(Vbus[t]) + YVsum) / Ybus[t, t]
#                     error[t, :] = [abs(Vbus[t]) - abs(Vbus_old), 0, 0]
#                 elif Qgen[t] < Qmin[t]:
#                     Qdelta[t] = Qmin[t] - Qdel[t]
#                     YVsum -= Ybus[t, t] * abs(Vbus[t])
#                     Vbus_old = Vbus[t]
#                     Vbus[t] = ((Pdelta[t] - 1j * Qdelta[t]) / abs(Vbus[t]) + YVsum) / Ybus[t, t]
#                     error[t, :] = [abs(Vbus[t]) - abs(Vbus_old), 0, 0]
#                 else:
#                     Qgen[t] = Qdelta[t] + Qdel[t]
#                     error[t, :] = [Qdelta[t] - Qdelta_old, 0, 0]
#         e = sum(e_ind)
#     return Vbus
