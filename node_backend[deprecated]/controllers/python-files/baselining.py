from Algorithms.Signal_Stats_Algo import SignalStats
import sys
import json
def read_data_from_file(data_file_path):
    with open(data_file_path, 'r') as file:
        data = json.load(file)
    return data

# if len(sys.argv) != 1:
#     print("Usage: python event-detection.py <data> <windowSize> <sd_th>")
#     sys.exit(1)
try:
    data= read_data_from_file(sys.argv[1])
    ss = SignalStats()
    res = ss.findStatistics(data)
    res = json.dumps(res)
    print(res)
except ValueError:
    print("Invalid argument format. Please provide valid arguments.")
    sys.exit(1)

