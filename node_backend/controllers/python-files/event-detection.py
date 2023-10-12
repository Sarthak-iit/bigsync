import sys 
import json
def listOfCharsToNumber(arr):
    for i in range(len(arr)):
        arr[i] = float(arr[i])
    return arr
from Algorithms.FD_Algo import FaultDetection

# Check if the script is called with the expected number of arguments
if len(sys.argv) != 5:
    print("Usage: python event-detection.py <data> <windowSize> <sd_th>")
    sys.exit(1)
try:
    data = listOfCharsToNumber((sys.argv[1]).split(','))
    time = listOfCharsToNumber((sys.argv[2]).split(','))
    window_size = float(sys.argv[3])
    sd_th = float(sys.argv[4])
    faultDetection = FaultDetection()
    res = faultDetection.getFault(data,time,window_size, sd_th)
    if(res):
        data_freq = res[0].tolist()
        data_rocof = res[1].tolist()
        data_time = res[2].tolist()
        res = {"fault": True, "freq": data_freq, "time": data_time, "rocof": data_rocof}
        # Serialize the dictionary to a JSON string
        res_json = json.dumps(res)
        print(res_json)
    else:
        print((json.dumps({"fault":False})))

except ValueError:
    print("Invalid argument format. Please provide valid arguments.")
    sys.exit(1)

