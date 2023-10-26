from algos.Algorithms.Signal_Stats_Algo import SignalStats
import sys
import json
def findStats(data):
    try:
        ss = SignalStats()
        res = ss.findStatistics(data)
        return(res)
    except:
        return {"error":"Something bad happened while baselining data"}

