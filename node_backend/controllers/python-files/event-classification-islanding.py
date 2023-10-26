import sys 
import json
from Algorithms.FC_Algo import EventClassification
def read_data_from_file(data_file_path):
    with open(data_file_path, 'r') as file:
        data = json.load(file)
    return data
# Check if the script is called with the expected number of arguments
if len(sys.argv) != 3:
    print("Usage: python event-classification.py <data> <windowSize> <sd_th>")
    sys.exit(1)
try:
    data_file_path = sys.argv[1]
    data_file = read_data_from_file(data_file_path)
    datas = data_file[0]
    time = data_file[1]
    threshold_values = json.loads(sys.argv[2])
    if time and datas:
        eventClassify =  EventClassification(datas,time,threshold_values)
        res = eventClassify.islandingEvent([time,datas])
        print(json.dumps(eventClassify.islandingEvent([time,datas])))
except ValueError:
    print("Invalid argument format. Please provide valid arguments.")
    sys.exit(1)

