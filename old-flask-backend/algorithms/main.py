import pandas as pd
import numpy as np
from flask import jsonify
import math
def removeNan(arr):
    curr = 60
    for i in range(len(arr)):
        if math.isnan(arr[i]) or arr[i] == 0:
            arr[i] = curr
        else:
            curr = arr[i]
    return arr
def is_array_of_numbers(arr):
    return all(isinstance(item, (int, float)) for item in arr)

class FaultDetection:
    def __init__(self):
        self._T = 0.02
        self._Q = np.array([[0.001, 0], [0, 1]])
        self._R = 0.01
        self._Xcap_ = np.array([[50, 0]]).T 
        self._Pk_ = np.array([[10, 0], [0, 10]])
        self._Ad = np.array([[1,self._T], [0, 1]])
        self._Cd = np.array([[1, 0]])
        self._Bd = np.array([[0, 0]])
    
    def _KalmanFilter(self,Vo):
        try:
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
        except Exception as e:
            # Handle the exception, log it, and return a generic error response
            print(f"An error occurred in _impulseEvent: {str(e)}")
            return jsonify({'error': 'An unexpected error occurred'}), 500
    
    def _movingvar(self,x, m):
        try:
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
        except Exception as e:
            print(f"An error occurred in _impulseEvent: {str(e)}")
            return jsonify({'error': 'An unexpected error occurred'}), 500

    
    def getFault(self,data,win_size,sd_th):
        try:
            self._rocof_sd_threshold = sd_th
            freq_data = data[0]
            time_data = data[1]
            time_data = time_data
            freq_data = removeNan(freq_data)
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
        except Exception as e:
            # Handle the exception, log it, and return a generic error response
            print(f"An error occurred in getFault: {str(e)}")
            return jsonify({'error': 'An unexpected error occurred'}), 500

class EventClassification(FaultDetection):
    def __init__(self,data):
        self._time_data = np.array(data[0]['time'])
        self._freq_data = removeNan(np.array(data[0]['data'])) if is_array_of_numbers(np.array(data[0]['data'])) else np.array(data[0]['data'])
        self._KalmanFilter = FaultDetection._KalmanFilter
        # Events
        self.isImpulseEvent = False
        self.isGenLossEvent = False
        self.isLoadLossEvent = False
        self.isOscillatoryEvent = False
        self.isIslandingEvent = False
        self.thresholdValues = data[2]

    #     const [thresholdValues, setThresholdValues] = useState({
    #     stepChange: 0.1,
    #     oscillatoryEvent: 5,
    #     impulseEvent: 2,
    #     islandingEvent: 0.1,
    #   });


    def _impulseEvent(self):
        try:
            time_data = self._time_data
            win_size = 10
            win_size = int(len(time_data)/((time_data[-1]-time_data[0])/win_size))
            duration = time_data[-1] - time_data[0]
            n_samples = len(time_data)
            k = duration/n_samples
            time_data = np.linspace(0,duration,n_samples)    
            i = 0
            print(self.thresholdValues)
            th_impulse = float(self.thresholdValues['impulseEvent'])
            while(i < len(self._freq_data)):
                curr_data = self._freq_data[i:i+win_size]
                kalman_filter_output = self._KalmanFilter(FaultDetection(),curr_data)
                rocof_data = kalman_filter_output[2]
                max_rocof = max(rocof_data)
                if((max_rocof)>th_impulse):
                    self.isImpulseEvent = True
                    return [rocof_data.tolist(),time_data[i:i+win_size].tolist()]
                i += win_size
            return []
        except Exception as e:
            # Handle the exception, log it, and return a generic error response
            print(f"An error occurred in _impulseEvent: {str(e)}")
            return jsonify({'error': 'An unexpected error occurred'}), 500

    def _stepChangeEvent(self):
        try:
            time_data = self._time_data
            win_size = 20
            win_size = int(len(time_data)/((time_data[-1]-time_data[0])/win_size))
            duration = time_data[-1] - time_data[0]
            n_samples = len(time_data)
            k = duration/n_samples
            time_data = np.linspace(0,duration,n_samples)    
            i = 0
            th_step = float(self.thresholdValues['stepChange'])
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
                if((t_max - t_min) > 10 and (f_max - f_min) > th_step):
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
        except Exception as e:
            # Handle the exception, log it, and return a generic error response
            print(f"An error occurred in _impulseEvent: {str(e)}")
            return jsonify({'error': 'An unexpected error occurred'}), 500
                
            
        return [[],[]]
    def _oscillatoryEvent(self):
        try:    
            P_th = float(self.thresholdValues['oscillatoryEvent'])
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
                kalman_filter_output = self._KalmanFilter(FaultDetection(),curr_data)
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
        except Exception as e:
            # Handle the exception, log it, and return a generic error response
            print(f"An error occurred in _impulseEvent: {str(e)}")
            return jsonify({'error': 'An unexpected error occurred'}), 500
        
    def islandingEvent(self,data):
        try:
            f_th =float(self.thresholdValues['islandingEvent'])
            time_data = data[0]
            freqs_data = data[1]
            for i in range(len(freqs_data)):
                print('HI')
                freqs_data[i] = removeNan(freqs_data[i])
            for x in range(len(freqs_data)):
                freqs_data[x] = freqs_data[x]
            win_size = 10
            win_size = int(len(time_data)/((time_data[-1]-time_data[0])/win_size))
            duration = time_data[-1] - time_data[0]
            n_samples = len(time_data)
            k = duration/n_samples
            time_data = np.linspace(0,duration,n_samples)    
            i = 0
            while(i < len(freqs_data[0])):
                # curr_data = self._freq_data[i:i+win_size]
                f_max_s = freqs_data[0][i]
                f_max_e = freqs_data[0][i+win_size-1]
                f_min_s = freqs_data[0][i]
                f_min_e = freqs_data[0][i+win_size-1]
                for j in range(len(freqs_data)):
                    f_max_s = max(freqs_data[j][i],f_max_s)
                    f_max_e = max(freqs_data[j][i+win_size-1],f_max_e)
                    f_min_s = min(freqs_data[j][i],f_min_s)
                    f_min_e = min(freqs_data[j][i+win_size-1],f_min_e)
                del_fs = f_max_s - f_min_s
                del_fe = f_max_e - f_min_e
                r = []
                print(f_max_s,f_max_e,f_min_s,f_min_e)
                if(del_fs < f_th and del_fe > f_th):
                    for x in range(len(freqs_data)):
                        r.append(freqs_data[x][i:i+win_size])
                    res = {"Impulse event":'NA',"Generation Loss Event":'NA',"Load Loss Event":'NA',"Oscillatory Event":'NA',"Islanding Event":True}
                    return {'data':[[[],[]],[[],[]],[r,time_data[i:i+win_size].tolist()],[[],[]],[[],[]]],'result':res}
                i += win_size
                res = {"Impulse event":'NA',"Generation Loss Event":'NA',"Load Loss Event":'NA',"Oscillatory Event":'NA',"Islanding Event":False}
                return {'data':[[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]],'result':res}

            return [[],[]]
        except Exception as e:
            # Handle the exception, log it, and return a generic error response
            print(f"An error occurred in _impulseEvent: {str(e)}")
            return jsonify({'error': 'An unexpected error occurred'}), 500
    
    def classifyEvents(self):
        try:
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
        except Exception as e:
            # Handle the exception, log it, and return a generic error response
            print(f"An error occurred in _impulseEvent: {str(e)}")
            return jsonify({'error': 'An unexpected error occurred'}), 500
        






