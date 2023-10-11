import sys 
import json

from Algorithms.FC_Algo import EventClassification
def listOfCharsToNumber(arr):
    for i in range(len(arr)):
        arr[i] = float(arr[i])
    return arr

if len(sys.argv) != 4:
    print("Usage: python event-classification.py <data> <windowSize> <sd_th>")
    sys.exit(1)
try:
    data = listOfCharsToNumber((sys.argv[1]).split(','))
    time = listOfCharsToNumber((sys.argv[2]).split(','))
    threshold_values = json.loads(sys.argv[3])
    if time and data:
        eventClassify =  EventClassification(data,time,threshold_values)
        print(json.dumps(eventClassify.classifyEvents()))
except ValueError:
    print("Invalid argument format. Please provide valid arguments.")
    sys.exit(1)

