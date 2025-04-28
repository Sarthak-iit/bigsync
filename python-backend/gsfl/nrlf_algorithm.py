import numpy as np
import time

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

def calculate_jacobian(G, B, V, theta, PQ_buses):
    """
    Calculate the Jacobian matrix
    
    Parameters:
    -----------
    G : numpy.ndarray
        Conductance matrix
    B : numpy.ndarray
        Susceptance matrix
    V : numpy.ndarray
        Voltage magnitudes
    theta : numpy.ndarray
        Voltage angles in radians
    PQ_buses : numpy.ndarray
        Indices of PQ buses
        
    Returns:
    --------
    numpy.ndarray
        Jacobian matrix
    """
    nbuses = len(V)
    nPQ = len(PQ_buses)
    
    # Initialize submatrices
    J1 = np.zeros((nbuses - 1, nbuses - 1))  # dP/dθ (excluding slack bus)
    J2 = np.zeros((nbuses - 1, nPQ))         # dP/dV
    J3 = np.zeros((nPQ, nbuses - 1))         # dQ/dθ
    J4 = np.zeros((nPQ, nPQ))                # dQ/dV
    
    # J1 - dP/dθ
    for k in range(1, nbuses):
        for j in range(1, nbuses):
            if j == k:  # Diagonal elements
                for m in range(nbuses):
                    J1[k-1, j-1] += V[k] * V[m] * (-G[k, m] * np.sin(theta[k] - theta[m]) + 
                                                   B[k, m] * np.cos(theta[k] - theta[m]))
                J1[k-1, j-1] -= V[k]**2 * B[k, k]
            else:  # Off-diagonal elements
                J1[k-1, j-1] = V[k] * V[j] * (G[k, j] * np.sin(theta[k] - theta[j]) - 
                                              B[k, j] * np.cos(theta[k] - theta[j]))
    
    # J2 - dP/dV
    for k in range(1, nbuses):
        for j in range(nPQ):
            m = PQ_buses[j]
            if m == k:  # Diagonal elements
                for m_idx in range(nbuses):
                    J2[k-1, j] += V[m_idx] * (G[k, m_idx] * np.cos(theta[k] - theta[m_idx]) + 
                                             B[k, m_idx] * np.sin(theta[k] - theta[m_idx]))
                J2[k-1, j] += V[k] * G[k, k]
            else:  # Off-diagonal elements
                J2[k-1, j] = V[k] * (G[k, m] * np.cos(theta[k] - theta[m]) + 
                                    B[k, m] * np.sin(theta[k] - theta[m]))
    
    # J3 - dQ/dθ
    for k in range(nPQ):
        n = PQ_buses[k]
        for j in range(1, nbuses):
            if j == n:  # Diagonal elements
                for m in range(nbuses):
                    J3[k, j-1] += V[n] * V[m] * (G[n, m] * np.cos(theta[n] - theta[m]) + 
                                               B[n, m] * np.sin(theta[n] - theta[m]))
                J3[k, j-1] -= V[n]**2 * G[n, n]
            else:  # Off-diagonal elements
                J3[k, j-1] = V[n] * V[j] * (-G[n, j] * np.cos(theta[n] - theta[j]) - 
                                          B[n, j] * np.sin(theta[n] - theta[j]))
    
    # J4 - dQ/dV
    for k in range(nPQ):
        n = PQ_buses[k]
        for j in range(nPQ):
            m = PQ_buses[j]
            if m == n:  # Diagonal elements
                for m_idx in range(nbuses):
                    J4[k, j] += V[m_idx] * (G[n, m_idx] * np.sin(theta[n] - theta[m_idx]) - 
                                          B[n, m_idx] * np.cos(theta[n] - theta[m_idx]))
                J4[k, j] -= V[n] * B[n, n]
            else:  # Off-diagonal elements
                J4[k, j] = V[n] * (G[n, m] * np.sin(theta[n] - theta[m]) - 
                                 B[n, m] * np.cos(theta[n] - theta[m]))
    
    # Combine submatrices to form the complete Jacobian
    J = np.block([[J1, J2], [J3, J4]])
    
    return J

def calculate_power(G, B, V, theta):
    """
    Calculate active and reactive power at each bus
    
    Parameters:
    -----------
    G : numpy.ndarray
        Conductance matrix
    B : numpy.ndarray
        Susceptance matrix
    V : numpy.ndarray
        Voltage magnitudes
    theta : numpy.ndarray
        Voltage angles
        
    Returns:
    --------
    tuple
        (P_cal, Q_cal) calculated active and reactive powers
    """
    nbuses = len(V)
    P_cal = np.zeros(nbuses)
    Q_cal = np.zeros(nbuses)
    
    for k in range(nbuses):
        for m in range(nbuses):
            angle_diff = theta[k] - theta[m]
            P_cal[k] += V[k] * V[m] * (G[k, m] * np.cos(angle_diff) + B[k, m] * np.sin(angle_diff))
            Q_cal[k] += V[k] * V[m] * (G[k, m] * np.sin(angle_diff) - B[k, m] * np.cos(angle_diff))
    
    return P_cal, Q_cal

def calculate_mismatch(P_specified, Q_specified, P_cal, Q_cal, PQ_buses):
    """
    Calculate power mismatches
    
    Parameters:
    -----------
    P_specified : numpy.ndarray
        Net specified active power
    Q_specified : numpy.ndarray
        Net specified reactive power
    P_cal : numpy.ndarray
        Calculated active power
    Q_cal : numpy.ndarray
        Calculated reactive power
    PQ_buses : numpy.ndarray
        Indices of PQ buses
        
    Returns:
    --------
    numpy.ndarray
        Mismatch vector
    """
    nbuses = len(P_specified)
    nPQ = len(PQ_buses)
    
    # Calculate power differences
    dP = P_specified - P_cal
    dQ = Q_specified - Q_cal
    
    # Extract mismatch for PQ buses
    dQ_PQ = np.zeros(nPQ)
    for k in range(nPQ):
        dQ_PQ[k] = dQ[PQ_buses[k]]
    
    # Build mismatch vector (exclude slack bus for P)
    dP_nonslack = dP[1:nbuses]
    
    # Combine mismatches
    mismatch = np.concatenate((dP_nonslack, dQ_PQ))
    
    return mismatch

def perform_newton_raphson(line_data, bus_data, tol=1e-6, max_iter=20):
    """
    Perform load flow analysis using Newton-Raphson method
    
    Parameters:
    -----------
    bus_data : numpy.ndarray
        Bus data with format:
        [bus_id, V, theta, P_gen, Q_gen, P_load, Q_load, G_shunt, B_shunt, bus_type]
        where bus_type: 1=slack, 2=PV, 3=PQ
    line_data : numpy.ndarray
        Line data with format:
        [from_bus, to_bus, R, X, B, tap_ratio]
    tol : float, optional
        Convergence tolerance
    max_iter : int, optional
        Maximum number of iterations
        
    Returns:
    --------
    dict
        Load flow results
    """
    # Initial setup
    nbuses = len(bus_data[:, 0])
    
    # Calculate admittance matrix
    Y = calculate_Y_bus(line_data)
    G = np.real(Y)  # Conductance matrix
    B = np.imag(Y)  # Susceptance matrix
    
    # Initial voltage and angle values
    V = bus_data[:, 1].copy()      # Voltage magnitudes
    theta = bus_data[:, 2].copy()  # Voltage angles
    
    # Net specified power (Generation - Load)
    P_specified = bus_data[:, 3] - bus_data[:, 5]
    Q_specified = bus_data[:, 4] - bus_data[:, 6]
    
    # Identify bus types
    slack_buses = np.where(bus_data[:, 7] == 1)[0]
    PV_buses = np.where(bus_data[:, 7] == 2)[0]
    PQ_buses = np.where(bus_data[:, 7] == 3)[0]
    nPQ = len(PQ_buses)
    
    # Newton-Raphson iteration
    current_iter = 0
    error = 1.0
    start_time = time.time()
    
    while error > tol and current_iter < max_iter:
        # Calculate power
        P_cal, Q_cal = calculate_power(G, B, V, theta)
        
        # Calculate mismatch
        mismatch = calculate_mismatch(P_specified, Q_specified, P_cal, Q_cal, PQ_buses)
        
        # Check convergence
        error = np.max(np.abs(mismatch))
        if error <= tol:
            break
        
        # Build Jacobian
        J = calculate_jacobian(G, B, V, theta, PQ_buses)
        
        # Solve for corrections
        try:
            corrections = np.linalg.solve(J, mismatch)
        except np.linalg.LinAlgError:
            return {"error": "Singular Jacobian matrix encountered"}
        
        # Apply corrections
        dtheta = corrections[:nbuses-1]
        dV = corrections[nbuses-1:]
        
        # Update angles (excluding slack bus)
        theta[1:nbuses] += dtheta
        
        # Update voltages (PQ buses only)
        for i, bus_idx in enumerate(PQ_buses):
            V[bus_idx] += dV[i]
        
        current_iter += 1
    
    computation_time = time.time() - start_time
    
    # Calculate final values
    complex_voltages = V * np.exp(1j * theta)
    
    # Calculate power flows
    P_cal, Q_cal = calculate_power(G, B, V, theta)
    
    # Calculate line flows and losses
    line_flows = calculate_line_flows(line_data, complex_voltages)
    
    Vbus_results = [{"magnitude": mag, "angle": angle, "real_power": rp, "complex_power" : cp} for mag, angle,rp,cp in zip(V, np.degrees(theta),P_cal,Q_cal)]
    
    mismatch = calculate_mismatch(P_specified, Q_specified, P_cal, Q_cal, PQ_buses)
    error = np.max(np.abs(mismatch))
    return {"final_voltages": Vbus_results,
            "line_flow_results":line_flows,
            "iterations": current_iter,
            "max_mismatch": error}
    
    # # Prepare results
    # results = {
    #     "converged": error <= tol,
    #     "iterations": current_iter,
    #     "max_error": error,
    #     "computation_time": computation_time,
    #     "voltage_magnitude": V,
    #     "voltage_angle_rad": theta,
    #     "voltage_angle_deg": np.degrees(theta),
    #     "complex_voltages": complex_voltages,
    #     "active_power": P_cal,
    #     "reactive_power": Q_cal,
    #     "line_flows": line_flows
    # }
    
    return results

def calculate_line_flows(line_data, complex_voltages):
    """
    Calculate power flows in lines and transformers
    
    Parameters:
    -----------
    line_data : numpy.ndarray
        Line data
    complex_voltages : numpy.ndarray
        Complex bus voltages
        
    Returns:
    --------
    dict
        Line flows and losses
    """
    nbranch = len(line_data)
    print("LINE DATA:",line_data)
    
    # Initialize arrays
    from_bus_flows = np.zeros(nbranch, dtype=complex)
    to_bus_flows = np.zeros(nbranch, dtype=complex)
    
    for k in range(nbranch):
        from_idx = int(line_data[k, 1]) - 1  # Convert to 0-indexing
        to_idx = int(line_data[k, 2]) - 1    # Convert to 0-indexing
        r = line_data[k, 3]
        x = line_data[k, 4]
        b = line_data[k, 5]
        a = line_data[k, 6]  # Tap ratio
        
        # Line impedance and admittance
        z = complex(r, x)
        y = 1 / z
        print(np.isnan(a))
        if a == 0 or np.isnan(a):  # Transmission line
            # Line charging
            b_half = 1j * b / 2
            
            # Flow calculations
            from_bus_flows[k] = complex_voltages[from_idx] * np.conj(
                (complex_voltages[from_idx] - complex_voltages[to_idx]) * y + 
                complex_voltages[from_idx] * b_half
            )
            
            to_bus_flows[k] = complex_voltages[to_idx] * np.conj(
                (complex_voltages[to_idx] - complex_voltages[from_idx]) * y + 
                complex_voltages[to_idx] * b_half
            )
        else:  # Transformer
            # Equivalent circuit values
            y_prime = y / a
            from_shunt = (y_prime / a) * ((1 / a) - 1)
            to_shunt = y_prime * (1 - (1 / a))
            
            # Flow calculations
            from_bus_flows[k] = complex_voltages[from_idx] * np.conj(
                (complex_voltages[from_idx] - complex_voltages[to_idx]) * y_prime + 
                complex_voltages[from_idx] * from_shunt
            )
            
            to_bus_flows[k] = complex_voltages[to_idx] * np.conj(
                (complex_voltages[to_idx] - complex_voltages[from_idx]) * y_prime + 
                complex_voltages[to_idx] * to_shunt
            )
        # print("K=",k)
        # print("from_bus_flows:",from_bus_flows)
    
    # Calculate active and reactive flows
    P_from = np.real(from_bus_flows)
    Q_from = np.imag(from_bus_flows)
    P_to = np.real(to_bus_flows)
    Q_to = np.imag(to_bus_flows)
    
    # Calculate total system losses
    P_losses = np.sum(P_from + P_to)
    Q_losses = np.sum(Q_from + Q_to)
    
    line_flow_results = {
        "P_from": P_from,
        "Q_from": Q_from,
        "P_to": P_to,
        "Q_to": Q_to,
        "P_losses": P_losses,
        "Q_losses": Q_losses
    }
    temp_dict = {key: np.array(value).tolist() for key, value in line_flow_results.items()}
    
    final_line_flow = [{"from_bus":from_bus,
                       "to_bus":to_bus,
                       "P_from": p_from,
                       "Q_from": q_from,
                       "P_to": p_to,
                       "Q_to": q_to}
                       for from_bus, to_bus, p_from, q_from, p_to, q_to
                       in zip(np.array(line_data[:,1]).tolist(),np.array(line_data[:,2].tolist()),np.array(P_from.tolist()),np.array(Q_from.tolist()),np.array(P_to.tolist()),np.array(Q_to).tolist())
                       ]
    return final_line_flow