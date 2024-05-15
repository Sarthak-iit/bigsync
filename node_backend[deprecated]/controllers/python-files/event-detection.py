import sys 
import json
def read_data_from_file(data_file_path):
    with open(data_file_path, 'r') as file:
        data = json.load(file)
    return data
from Algorithms.FD_Algo import FaultDetection

# Check if the script is called with the expected number of arguments
if len(sys.argv) != 4:
    print("Usage: python event-detection.py <data> <windowSize> <sd_th>")
    sys.exit(1)
try:
    data_file_path = sys.argv[1]
    data_file = read_data_from_file(data_file_path)
    data = data_file[0]
    time = data_file[1]
    window_size = float(sys.argv[2])
    sd_th = float(sys.argv[3])
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

