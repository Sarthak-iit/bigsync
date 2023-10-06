import pandas as pd
import numpy as np
class FaultDetectionV1:
    def __init__(self):
        # initialising system parameters in contructor
        self._T = 0.02
        self._Q = np.array([[0.001, 0], [0, 1]])
        self._R = 0.01
        self._Xcap_ = np.array([[50, 0]]).T 
        self._Pk_ = np.array([[10, 0], [0, 10]])
        self._Ad = np.array([[1,self._T], [0, 1]])
        self._Cd = np.array([[1, 0]])
        self._Bd = np.array([[0, 0]])

    def _readCSV(self,file):
        data = pd.read_csv(file)

        time_data = data["time"].to_numpy().flatten()
        freq_data = data["frequency"].to_numpy().flatten()
        return [freq_data,time_data]
    
    def _KalmanFilter(self,Vo):
        N = len(Vo)
        m =int(1/self._T)
        k1 = np.arange(0, N)
        y = np.arange(0, N)
        xestimate = np.zeros((N, 2))
        for k in range(N):
            Yk = Vo[k]
            Xcap = (self._Ad @ self._Xcap_) #2x2 x 2x1 = 2x1
            Pk = (self._Ad @ self._Pk_ @ self._Ad.T) + self._Q
            K_ = (Pk @ self._Cd.T) / (self._Cd @ Pk @ self._Cd.T + self._R)
            self._Xcap_ = Xcap + K_*(Yk-(self._Cd@Xcap))
            self._Pk_ = Pk - (K_@self._Cd)@Pk
            xestimate[k, 0] = self._Xcap_[0]
            xestimate[k, 1] = self._Xcap_[1]
            k1[k] = k
            y[k] = Yk
        f_est = xestimate[:, 0]
        dfbydt_est = xestimate[:, 1]
        Mvar_dfbydt = self._movingvar(dfbydt_est,m)
        return [k1,f_est,dfbydt_est,Mvar_dfbydt]
    
    def _movingvar(self,x, m):
        n = x.shape[0]
        f = np.zeros(m)+  1/ m
        if len(x) == 0:
            return []
        v = np.convolve(x**2, f, mode='valid') - np.convolve(x, f, mode='valid')**2
        m2 = m // 2
        n2 = (m // 2) - 1
        start_idx = m2 + 1
        end_idx = n - n2
        v = v[start_idx:end_idx]
        return v

    
    def getFault(self,file,win_size,sd_th):
        data = self._readCSV(file)
        self._rocof_sd_threshold = sd_th
        print(self._rocof_sd_threshold)
        freq_data = data[0]
        time_data = data[1]
        print(type(win_size),type(freq_data),type(time_data))
        time_data = time_data
        freq_data = freq_data
        # getting window size of scanning from seconds provided by user
       
        win_size = int(len(time_data)/((time_data[-1]-time_data[0])/win_size))
        duration = time_data[-1] - time_data[0]
        n_samples = len(time_data)
        k = duration/n_samples
        time_data = np.linspace(0,duration,n_samples)    
        i = 0
        sd_rocof_data = []
        while(i < len(freq_data)):
            curr_data = freq_data[i:i+win_size]
            kalman_filter_output = self._KalmanFilter(curr_data)
            rocof_data = kalman_filter_output[2]
            sd_rocof = np.std(curr_data)
            if((sd_rocof)>self._rocof_sd_threshold):
                return [kalman_filter_output[1],rocof_data,time_data[i:i+win_size]]
            i += win_size
        return None

class EventClassificationV1(FaultDetectionV1):
    def __init__(self,file):
        self.file = file
        self._KalmanFilter = FaultDetectionV1._KalmanFilter
        # Events
        self.isImpulseEvent = False
        self.isGenLossEvent = False
        self.isLoadLossEvent = False
        self.isOscillatoryEvent = False
        self.isIslandingEvent = False
        self._rocof_th = 2
        self._readFile()

    def _readFile(self):
        file = self.file
        data = pd.read_csv(file)
        time_data = data["time"].to_numpy().flatten()
        freq_data = data["frequency"].to_numpy().flatten()
        self._freq_data = freq_data
        self._time_data = time_data

    def _impulseEvent(self):
        time_data = self._time_data
        win_size = 10
        win_size = int(len(time_data)/((time_data[-1]-time_data[0])/win_size))
        duration = time_data[-1] - time_data[0]
        n_samples = len(time_data)
        k = duration/n_samples
        time_data = np.linspace(0,duration,n_samples)    
        i = 0
        while(i < len(self._freq_data)):
            curr_data = self._freq_data[i:i+win_size]
            kalman_filter_output = self._KalmanFilter(FaultDetectionV1(),curr_data)
            rocof_data = kalman_filter_output[2]
            max_rocof = max(rocof_data)
            if((max_rocof)>self._rocof_th):
                self.isImpulseEvent = True
                return [rocof_data.tolist(),time_data[i:i+win_size].tolist()]
            i += win_size
        return []

    def _stepChangeEvent(self):
        time_data = self._time_data
        win_size = 20
        win_size = int(len(time_data)/((time_data[-1]-time_data[0])/win_size))
        duration = time_data[-1] - time_data[0]
        n_samples = len(time_data)
        k = duration/n_samples
        time_data = np.linspace(0,duration,n_samples)    
        i = 0
        while(i < len(self._freq_data)):
            curr_data = np.array(self._freq_data[i:i+win_size])
            curr_time_data = np.array(self._time_data[i:i+win_size])
            f_max_index = np.argmax(curr_data)
            f_max = curr_data[f_max_index]
            t_max = curr_time_data[f_max_index]
            f_min_index = np.argmin(curr_data)
            f_min = curr_data[f_min_index]
            t_min = curr_time_data[f_min_index]
            # 
            if((t_max - t_min) > 10 and (f_max - f_min) > 0.1):
                print("t_max, t_min",t_max,t_min)
                print("f_max, f_min",f_max,f_min)
                gradient = np.gradient(curr_data)
                slope_avg = np.mean(gradient)
                if slope_avg > 0:
                    self.isGenLossEvent = True
                    return [curr_data.tolist(),time_data[i:i+win_size].tolist(),'gen']
                else:
                    self.isLoadLossEvent = True
                    return [curr_data.tolist(),time_data[i:i+win_size].tolist(),'load']
                
            i += win_size
            
            
        return [[],[]]
    def _oscillatoryEvent(self):
        P_th = 5
        time_data = self._time_data
        fs = 1/(time_data[1] - time_data[0])
        win_size = 10
        win_size = int(len(time_data)/((time_data[-1]-time_data[0])/win_size))
        duration = time_data[-1] - time_data[0]
        n_samples = len(time_data)
        k = duration/n_samples
        time_data = np.linspace(0,duration,n_samples)    
        i = 0
        while(i < len(self._freq_data)):
            curr_data = self._freq_data[i:i+win_size]
            kalman_filter_output = self._KalmanFilter(FaultDetectionV1(),curr_data)
            rocof_data = kalman_filter_output[2]
            fft_result = np.fft.fft(rocof_data)
            power_spectrum = np.abs(fft_result) ** 2
            power_spectrum_db = 10 * np.log10(power_spectrum)
            frequencies = np.fft.fftfreq(len(fft_result), 1 / fs)
            for j in range(len(frequencies)):
                f = frequencies[j]
                if f < 0.05:
                    continue
                elif f>4:
                    break
                else:
                    if power_spectrum_db[j] > P_th:
                        self.isOscillatoryEvent = True
                        return [power_spectrum_db.tolist(),frequencies.tolist()]
            i += win_size
        return [[],[]]
    def islandingEvent(self,data):
        return [[],[]]
    
    def classifyEvents(self):
        impulse_data = self._impulseEvent()
        stepChangeData = self._stepChangeEvent()
        if stepChangeData[-1] == 'gen':
            genLossEventData = stepChangeData[:len(stepChangeData)-1]
            loadLossEventData = [[],[]]
        else:
            loadLossEventData = stepChangeData[:len(stepChangeData)-1]
            genLossEventData = [[],[]]
        oscialltoryEventData = self._oscillatoryEvent()
        islandingData = [[],[]]
        res = {"Impulse event":self.isImpulseEvent,"Generation Loss Event":self.isGenLossEvent,"Load Loss Event":self.isLoadLossEvent,"Oscillatory Event":self.isOscillatoryEvent,"Islanding Event":'NA'}
        return {'data':[genLossEventData,impulse_data,islandingData,loadLossEventData,oscialltoryEventData],'result':res}    
        






