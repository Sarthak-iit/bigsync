import numpy as np
from gsfl.gsfl_algorithm import calculate_Y_bus

def perform_dclf(line_data, bus_data):
    # Number of lines
    n_lines = int(np.max(line_data[:, 0]))
    
    Nmax = np.max(line_data[:, 1:3])
    n_buses = int(Nmax)
    
    # neglect resistance of the transmission lines
    line_data[:,3] = 0
    
    Y = calculate_Y_bus(line_data)
    print(Y)
    y = Y[1:, 1:]
    
    # Net power (Generation - Load)
    P_neta = bus_data[:,3] - bus_data[:,5]
    # from the P_neta vector also erease the P of the slack bus
    P_neta = P_neta[1:]
    # compute the angles of the nodes using the imaginary part of the y matrix
    Theta = np.matmul(np.linalg.inv(np.imag(y)),P_neta)
    # It is assumed tha the slack bus has an angle of zero
    Theta = np.concatenate(([0],Theta))
    # compute the power injections at each node
    Pi = np.matmul(np.imag(Y),Theta)
    # compute the line flows
    # voltage of buses are equal to one
    V = np.ones((n_buses,1))
    ## calculate the line flows and power losses
    FromNode=line_data[:,1]
    ToNode=line_data[:,2]
    # define active power flows
    Pij = np.zeros(n_lines)
    Pji = np.zeros(n_lines)
    for k in range(n_lines):
        # print(FromNode[k])
        # print(ToNode[k])
        # print(Y[int(FromNode[k]),int(ToNode[k])])
        # print(Theta[FromNode[k]-ToNode[k]])
        Pij[k] = np.imag(Y[int(FromNode[k])-1,int(ToNode[k])-1])*(Theta[int(FromNode[k])-1]-Theta[int(ToNode[k])-1])
    for k in range(n_lines):
        
        Pji[k] = np.imag(Y[int(ToNode[k])-1,int(FromNode[k])-1])*(Theta[int(ToNode[k])-1]-Theta[int(FromNode[k])-1])
    
    # y = Y.copy()
    # y = np.delete(y, 0, axis=0)
    # y = np.delete(y, 0, axis=1)
    
    # P_neta = bus_data[:, 3] - bus_data[:, 5]  # Pg - Pl
    # P_neta = np.delete(P_neta, 0)
    
    # Theta = np.linalg.inv(np.imag(y)) @ P_neta
    # Theta = np.insert(Theta, 0, 0.0)
    
    # Pi = np.imag(Y @ Theta)
    # V = np.ones(n_buses)
    
    # FromNode = line_data[:, 0].astype(int)
    # ToNode = line_data[:, 1].astype(int)
    
    # Pij = []
    # Pji = []
    
    # for k in range(len(line_data)):
    #     i = FromNode[k] - 1
    #     j = ToNode[k] - 1
    #     val = np.imag(Y[i, j]) * (Theta[i] - Theta[j])
    #     Pij.append(val)
    
    # for k in range(len(line_data)):
    #     j = FromNode[k] - 1
    #     i = ToNode[k] - 1
    #     val = np.imag(Y[i, j]) * (Theta[i] - Theta[j])
    #     Pji.append(val)
    
    # Compose output
    voltages = [
        {"magnitude": 1.0, "angle": float(np.degrees(th)), "real_power": float(np.real(pi)), "complex_power": 0.0 }
        for th, pi in zip(Theta, Pi)
    ]
    
    
    line_flow_results = [
        {
            "from_bus": int(FromNode[i]),
            "to_bus": int(ToNode[i]),
            "P_from": float(Pij[i]),
            "P_to": float(Pji[i]),
            "P_losses": 0.0,
            "Q_losses": 0.0
        }
        for i in range(n_lines)
    ]
    
    return {
        "final_voltages": voltages,
        "line_flow_results": line_flow_results,
        "iterations": 1,
        "max_mismatch": 0.0
    }
