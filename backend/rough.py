import pandas as pd
from algorithms.main import FaultDetection 
from algorithms.main import EventClassification

a = EventClassification('/Users/rishavkumar/Desktop/BTP/testing_files/test1/f1.csv',2)
print(a.classifyEvents())