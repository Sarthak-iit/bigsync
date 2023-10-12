import numpy as np
import json

class SignalStats:
    def findStatistics(self,data):
        try:
            if len(data) == 0:
                return None  # Return None for an empty dataset
            
            min_value = np.min(data)
            max_value = np.max(data)
            mean = np.mean(data)
            percentile_995 = np.percentile(data, 0.5)
            percentile_999 = np.percentile(data, 0.1)
            return {
                "Minimum": min_value,
                "Maximum": max_value,
                "Mean": mean,
                "99.5% Limit": percentile_995,
                "99.9% Limit": percentile_999
            }
            
        except Exception as e:
            # Handle the exception, log it, and return a generic error response
            print(f"{'error': 'An unexpected error occurred'}")
    
    