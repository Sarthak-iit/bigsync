import numpy as np
import pandas as pd
from main import FaultDetection
class EventClassification(FaultDetection):
    def __init__(self,file,window_size):
        self.file = file
        self._KalmanFilter = FaultDetection._KalmanFilter
        self.isImpulseEvent = False
        self._rocof_th = 2
        self.window_size = window_size
        self._readFile()

    def _readFile(self):
        file = self.file
        data = pd.read_csv(file)
        freq_data = data["time"].to_numpy().flatten()
        time_data = data["frequency"].to_numpy().flatten()
        self.freq_data = freq_data
        self.time_data = time_data

    def _impulseEvent(self):
        win_size = int(len(time_data)/((time_data[-1]-time_data[0])/win_size))
        duration = time_data[-1] - time_data[0]
        n_samples = len(time_data)
        k = duration/n_samples
        time_data = np.linspace(0,duration,n_samples)    
        i = 0
        while(i < len(self._freq_data)):
            curr_data = self._freq_data[i:i+win_size]
            kalman_filter_output = self._KalmanFilter(curr_data)
            rocof_data = kalman_filter_output[2]
            max_rocof = max(rocof_data)
            if((max_rocof)>self._rocof_th):
                self.isImpulseEvent = True
                return None
            i += win_size
        return None
    
        

