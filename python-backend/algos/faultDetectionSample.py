import pandas as pd
import numpy as np
from .Algorithms.FaultClassification.DownSample import downsample_array

def faultClassificationSampleToSample(excel_data, threshold):
    # Load the Excel file
    fault_data = excel_data
    fault_data.to_csv()
    fault_data.columns = fault_data.columns.str.strip()

    # Extract time and current columns
    time = fault_data["Domain"].values  # Time column
    IA = fault_data["IA"].values        # Phase A Current
    IB = fault_data["IB"].values        # Phase B Current
    IC = fault_data["IC"].values        # Phase C Current

    def detect_faults(time, data):
        faults = []
        mn_tm = None
        mx_tm = None

        for i in range(1, len(data)):
            if abs(data[i] - data[i-1]) > threshold:
                if mn_tm is None:
                    mn_tm = time[i]  # First fault occurrence
                mx_tm = time[i]  # Update last fault occurrence

        # If no fault is found, return None to indicate it
        return mn_tm, mx_tm


    # Detect faults for each phase
    mn_tm_a, mx_tm_a = detect_faults(time, IA)
    mn_tm_b, mx_tm_b = detect_faults(time, IB)
    mn_tm_c, mx_tm_c = detect_faults(time, IC)

    # Determine the first and last fault occurrence across all phases
    mn_time = min(filter(None, [mn_tm_a, mn_tm_b, mn_tm_c]), default=None)
    mx_time = max(filter(None, [mx_tm_a, mx_tm_b, mx_tm_c]), default=None)

    # print((len(fault_data)-1)/(fault_data['Domain'].iloc[-1]-fault_data['Domain'].iloc[0]))

    # Return results
    if mn_time is not None and mx_time is not None:
        return {
            "status": "Fault detected",
            "fault_start": mn_time, 
            "fault_end": mx_time,
            "domain": downsample_array(time).tolist(),
            "IA": downsample_array(IA).tolist(),
            "IB": downsample_array(IB).tolist(),
            "IC": downsample_array(IC).tolist(),
        }
    else:
        return {
            "status": "No Fault detected",
            "fault_start": mn_time, 
            "fault_end": mx_time,
            "domain": downsample_array(time).tolist(),
            "IA": downsample_array(IA).tolist(),
            "IB": downsample_array(IB).tolist(),
            "IC": downsample_array(IC).tolist(),
        }
