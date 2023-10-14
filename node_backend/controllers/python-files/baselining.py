from Algorithms.Signal_Stats_Algo import SignalStats
import sys
import json
if len(sys.argv) != 2:
    print("Usage: python event-detection.py <data> <windowSize> <sd_th>")
    sys.exit(1)
try:
    data = json.loads(sys.argv[1])
    ss = SignalStats()
    res = ss.findStatistics(data)
    res = json.dumps(res)
    print(res)
except ValueError:
    print("Invalid argument format. Please provide valid arguments.")
    sys.exit(1)

