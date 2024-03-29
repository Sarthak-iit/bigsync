import sys 
import json
from algos.Algorithms.Faults.FC_Algo import EventClassification

def classifyIslandingEvent(datas,time,threshold_values):
    try:
        if time and datas:
            eventClassify =  EventClassification(datas,time,threshold_values)
            res = eventClassify.islandingEvent([time,datas])
            return(res)
    except:
        return({"error":"Something went wrong while classifying islanding event"})

