import sys 
import json
from Algorithms.FC_Algo import EventClassification

def listOfCharsToNumber(arr):
    for i in range(len(arr)):
        arr[i] = float(arr[i])
    return arr
# Check if the script is called with the expected number of arguments
if len(sys.argv) != 4:
    print("Usage: python event-classification.py <data> <windowSize> <sd_th>")
    sys.exit(1)
try:
    datas = json.loads((sys.argv[1]))
    time = listOfCharsToNumber((sys.argv[2]).split(','))
    threshold_values = json.loads(sys.argv[3])
    if time and datas:
        eventClassify =  EventClassification(datas,time,threshold_values)
        res = eventClassify.islandingEvent([time,datas])
        print(json.dumps(eventClassify.islandingEvent([time,datas])))
except ValueError:
    print("Invalid argument format. Please provide valid arguments.")
    sys.exit(1)

