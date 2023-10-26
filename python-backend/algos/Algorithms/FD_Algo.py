import numpy as np
import math
def removeNan(arr):
    curr = 60
    for i in range(len(arr)):
        if math.isnan(arr[i]) or arr[i] == 0:
            arr[i] = curr
        else:
            curr = arr[i]
    return arr

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
            print(f"{'error': 'An unexpected error occurred'}")
    
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
            print(f"{'error': 'An unexpected error occurred'}")

    
    def getFault(self,data,time,win_size,sd_th):
        try:
            self._rocof_sd_threshold = sd_th
            freq_data = data
            time_data = time
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
                sd_rocof = np.std(rocof_data)
                if((sd_rocof)>self._rocof_sd_threshold):
                    return [kalman_filter_output[1],rocof_data,time_data[i:i+win_size]]
                i += win_size
            return None
        except Exception as e:
            # Handle the exception, log it, and return a generic error response
            print(f"{'error': 'An unexpected error occurred'}")
            