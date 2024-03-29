import sys 
import json
from algos.Algorithms.Faults.FD_Algo import FaultDetection

# Check if the script is called with the expected number of arguments
def eventDetection(data,time,window_size,sd_th):
    try:
        faultDetection = FaultDetection()
        res = faultDetection.getFault(data,time,window_size, sd_th)
        if(res):
            data_freq = res[0].tolist()
            data_rocof = res[1].tolist()
            data_time = res[2].tolist()
            res = {"fault": True, "freq": data_freq, "time": data_time, "rocof": data_rocof}
            return res
        else:
            return {"fault":False}

    except:
        return {"error": "Something bad happened in server while detecting fault"}
        # sys.exit(1)

