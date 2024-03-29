import sys 
import json

from algos.Algorithms.Faults.FC_Algo import EventClassification
def read_data_from_file(data_file_path):
    with open(data_file_path, 'r') as file:
        data = json.load(file)
    return data

def eventClassification(data,time,threshold_values):
    try:
        if time and data:
            eventClassify =  EventClassification(data,time,threshold_values)
            return(json.loads(eventClassify.classifyEvents()))
    except:
        return {"error":"Some error happended while classifying event"}

