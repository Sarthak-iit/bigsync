import numpy as np
import pandas as pd
from .Algorithms.FaultClassification.DownSample import downsample_array

def faultClassificationSequenceComponents(excel_data, sim_duration, faultInsatant, faultTime):
    fault_data = excel_data
    fault_data.to_csv()
    fault_data.columns = fault_data.columns.str.strip()

    Domain = fault_data['Domain'].values
    IA = fault_data['IA'].values
    IB = fault_data['IB'].values
    IC = fault_data['IC'].values

################################   DFT   ################################    

    num_rows = len(IA)

    # Make N dynamic: Take the smaller of 1666 or num_rows//2 (at least 2 cycles if possible)
    N = min(int(1.6667e3), max(num_rows // 2, 1))  

    # Scaling factor remains the same
    scaling_factor = (1 / 60) / N  

    # Time domain reference
    t = Domain
    phase_angle = np.angle(np.exp(1j * 2 * np.pi * 60 * t)) * 180 / np.pi

    # Adjust Domain to match computed values
    if num_rows > N:
        Domain = Domain[N//2 : num_rows - N//2]  
    else:
        Domain = Domain  # Keep as is if too few samples

    # Function to compute RMS and Theta
    def compute_rms_and_theta(In):
        Irms_list = []
        theta_list = []

        # Precompute cosine and sine terms
        cos_terms = np.cos(2 * np.pi * np.arange(N) / N)
        sin_terms = np.sin(2 * np.pi * np.arange(N) / N)

        for j in range(num_rows - N):
            window = In[j:j + N]
            Ir = np.sum(window * cos_terms)
            Ii = np.sum(window * sin_terms)
            Irms_list.append(np.sqrt(Ir ** 2 + Ii ** 2) * (np.sqrt(2) / N))
            theta_list.append(-np.degrees(np.arctan2(Ii, Ir)))

        return np.array(Irms_list), np.array(theta_list)

    # Compute for IA, IB, IC
    if num_rows > N:
        Iarms, Iatheta = compute_rms_and_theta(IA)
        Ibrms, Ibtheta = compute_rms_and_theta(IB)
        Icrms, Ictheta = compute_rms_and_theta(IC)
    else:
        Iarms, Iatheta, Ibrms, Ibtheta, Icrms, Ictheta = [], [], [], [], [], []

    # Remove unwanted phase angle range if applicable
    if len(phase_angle) > 100000:
        phase_angle = np.delete(phase_angle, slice(99994, 100001))

    # Adjust theta values with phase reference
    def wrap_to_180(angle):
        """Wrap angles to [-180, 180] range."""
        return ((angle + 180) % 360) - 180

    def adjusted_theta(theta_list, phase_angle):
        """Return adjusted theta values by subtracting the reference phase."""
        return wrap_to_180(theta_list - phase_angle[:len(theta_list)])

    if num_rows > N:
        Iatheta = adjusted_theta(Iatheta, phase_angle)
        Ibtheta = adjusted_theta(Ibtheta, phase_angle)
        Ictheta = adjusted_theta(Ictheta, phase_angle)

################################   DFT   ################################ 


    #To cal angle difference in range [0, 360)
    def angle_difference(I1, I2):
        # Get the angles in radians
        angle_I1 = np.angle(I1)
        angle_I2 = np.angle(I2)
        
        # Calculate the difference between the angles
        angle_diff_rad = angle_I2 - angle_I1
        
        # Convert the difference to degrees
        angle_diff_deg = np.rad2deg(angle_diff_rad)
        
        # Normalize the angle to the range [0, 360) degrees
        angle_diff_normalized = angle_diff_deg % 360

        return angle_diff_normalized

################################   Coverting to Sequence   ################################ 

    # To covert polar to rectangular form for ease of caluclation 
    def polar_to_complex(magnitude, phase_degrees):
        phase_radians = np.radians(phase_degrees)
        return magnitude * np.exp(1j * phase_radians)
    
    def phase_to_sequence_components(Ia, Ib, Ic):
        I_abc = np.array([Ia, Ib, Ic], dtype=complex)

        # Define the operator a (120-degree phase shift)
        a = np.exp(2j * np.pi / 3)
        a2 = a ** 2

        # Transformation matrix for sequence components
        A = np.array([
            [1, 1, 1],
            [1, a, a2],
            [1, a2, a]
        ], dtype=complex)

        # Compute sequence components
        I_seq = (1 / 3) * (A @ I_abc)
        I0, I1, I2 = I_seq
        return I0, I1, I2
    
    sequence_components = []

    for i in range(len(Iarms)):
        # Use adjusted phases for computation
        Ia = polar_to_complex(Iarms[i], Iatheta[i])
        Ib = polar_to_complex(Ibrms[i], Ibtheta[i])
        Ic = polar_to_complex(Icrms[i], Ictheta[i])

        # Compute sequence components
        I0, I1, I2 = phase_to_sequence_components(Ia, Ib, Ic)
        sequence_components.append((I0, I1, I2))

    # Extract individual sequence components
    I0, I1, I2 = zip(*sequence_components)

################################   Coverting to Sequence   ################################


    ag = 0
    bg = 0
    cg = 0
    ab = 0
    bc = 0
    ca = 0
    abg = 0
    bcg = 0
    cag = 0
    abc = 0
    err = 0

    sim_dur = sim_duration
    fault_start = faultInsatant
    falut_duration = faultTime
    fault_end = fault_start + falut_duration
    pre_fault_time = 0.2



    for i in range(0, len(Domain)):
        if (Domain[i] >= pre_fault_time and (Domain[i] < fault_start or Domain[i] > fault_end)):
            I1_pre = I1[i]
            break

    

    # Traversing the data for falut analysis
    for i in range(0, len(Domain)):
        if (Domain[i] >= fault_start and Domain[i] <= fault_end):
            # if(i >= len(I1)):
            #     continue
            # Input for positive sequence current
            # I0_fault, I1_fault, I2_fault = phase_to_sequence_components(fft_IA[i], fft_IB[i], fft_IC[i])

            # magnitude_I0_fault = magnitude_I0[i]
            # phase_I0_fault = phase_I0[i]
            # magnitude_I1_fault = magnitude_I1[i]
            # phase_I1_fault = phase_I1[i]
            # magnitude_I2_fault = magnitude_I2[i]
            # phase_I2_fault = phase_I2[i]

            I1_fault = I1[i]
            I2_fault = I2[i]
            I0_fault = I0[i]

            # Convertion to rectangular form for ease of calculation
            I1_f = I1_fault - I1_pre
            I2_f = I2_fault
            I0_f = I0_fault


            # Calculating delta positive and delta zero
            delta_pos = angle_difference(I1_f, I2_f)
            delta_zero = angle_difference(I0_f, I2_f)

            #Fault Classification:

            #For 3-phase abc fault
            if(np.abs(I2_f) <= 1e-4 and np.abs(I0_f) <= 1e-4):
                # print("The fault type is balanced 3-phase abc")
                abc += 1

            #For ag fault
            elif ((delta_pos >= 0 and delta_pos <= 15) or (delta_pos >= 345 and delta_pos <= 360)) and ((delta_zero >= 0 and delta_zero <= 30) or (delta_zero >= 330 and delta_zero <= 360)):
                # print("The falut tpye is ag")
                ag += 1

            #For ab and abg fault
            elif delta_pos >= 45 and delta_pos <= 75:
                #For abg fault
                if delta_zero >= 90 and delta_zero <= 150:
                    # print("The fault is abg")
                    abg += 1
                #For ab fault
                else:
                    # print("The fault is ab")
                    ab += 1

            #For bg fault 
            elif (delta_pos >= 105 and delta_pos <= 135) and (delta_zero >= 210 and delta_zero <= 270):
                # print("The falut tpye is bg")
                bg += 1

            #For bc and bcg fault
            elif delta_pos >= 165 and delta_pos <= 195:
                #For bcg fault
                if (delta_zero >= 0 and delta_zero <= 30) or (delta_zero >= 330 and delta_zero <= 360): 
                    # print("The fault is bcg")
                    bcg += 1
                #For bc fault
                else:
                    # print("The fault is bc")
                    bc += 1

            #For cg fault
            elif (delta_pos >= 225 and delta_pos <= 255) and (delta_zero >= 90 and delta_zero <= 150):
                # print("The falut tpye is cg")
                cg += 1

            #For ca and cag fault
            elif delta_pos >= 285 and delta_pos <= 315:
                if delta_zero >= 210 and delta_zero <= 270:
                    # print("The fault is cag")
                    cag += 1
                else:
                    # print("The fault is ca")
                    ca += 1

            else:
                # print("No fault detected")
                err += 1

    # print(f"fault of ag is {ag}")
    # print(f"fault of bg is {bg}")
    # print(f"fault of cg is {cg}")
    # print(f"fault of ab is {ab}")
    # print(f"fault of bc is {bc}")
    # print(f"fault of ca is {ca}")
    # print(f"fault of abg is {abg}")
    # print(f"fault of bcg is {bcg}")
    # print(f"fault of cag is {cag}")
    # print(f"fault of abc is {abc}")
    # print(f"No falut occurence is {err}")

    final_fault = [[ag, 'ag'], [bg, 'bg'], [cg, 'cg'], [ab, 'ab'], [bc, 'bc'], [ca, 'ca'], [abg, 'abg'], [bcg, 'bcg'], [cag, 'cag'], [abc, 'abc'], [err, 'No Fault']]

    final_fault.sort(reverse=True)

    return {
        "result": f"The fault is {final_fault[0][1].upper()}",
        "domain": downsample_array(Domain).tolist(),
        "I0m": downsample_array(np.abs(I0)).tolist(),
        "I1m": downsample_array(np.abs(I1)).tolist(),
        "I2m": downsample_array(np.abs(I2)).tolist(),
        "Iam": downsample_array(Iarms).tolist(),
        "Ibm": downsample_array(Ibrms).tolist(),
        "Icm": downsample_array(Icrms).tolist(),
        "I0a": downsample_array(np.angle(I0)).tolist(),
        "I1a": downsample_array(np.angle(I1)).tolist(),
        "I2a": downsample_array(np.angle(I2)).tolist(),
        "Iaa": downsample_array(Iatheta).tolist(),
        "Iba": downsample_array(Ibtheta).tolist(),
        "Ica": downsample_array(Ictheta).tolist(),
    }

    
