import numpy as np
import json
import math
from algos.Algorithms.Faults.FD_Algo import FaultDetection
faultDetection = FaultDetection()
def removeNan(arr):
    curr = 60
    for i in range(len(arr)):
        if math.isnan(arr[i]) or arr[i] == 0:
            arr[i] = curr
        else:
            curr = arr[i]
    return arr
class SignalStats:
    def findStatistics(self,data):
        try:
            if len(data) == 0:
                return None  # Return None for an empty dataset
            data = removeNan(data)
            rocof = self.testForRocof(data)
            min_value_freq = np.min(data)
            max_value_freq = np.max(data)
            mean_freq = np.mean(data)
            percentile_995_freq = np.percentile(data, 0.5)
            percentile_999_freq = np.percentile(data, 0.1)

            #for rocof
            min_value_rocof= np.min(rocof)
            max_value_rocof= np.max(rocof)
            mean_rocof= np.mean(rocof)
            percentile_995_rocof= np.percentile(rocof, 0.5)
            percentile_999_rocof= np.percentile(rocof, 0.1)
            return {
                'freq':
                    {"Minimum": min_value_freq,
                    "Maximum": max_value_freq,
                    "Mean": mean_freq,
                    "99.5% Limit": percentile_995_freq,
                    "99.9% Limit": percentile_999_freq},
                'rocof':
                    {"Minimum": abs(min_value_rocof),
                    "Maximum": abs(max_value_rocof),
                    "Mean": abs(mean_rocof),
                    "99.5% Limit": abs(percentile_995_rocof),
                    "99.9% Limit": abs(percentile_999_rocof)}
            }
        except Exception as e:
            print(f"{'error': 'An unexpected error occurred'}")
    def testForRocof(self,freq_data):
        try:
            kalman_filter_output = faultDetection._KalmanFilter(freq_data)
            rocof_data = kalman_filter_output[2]
            return rocof_data
        except Exception as e:
            print(f"{'error': 'An unexpected error occurred'}")
            
        