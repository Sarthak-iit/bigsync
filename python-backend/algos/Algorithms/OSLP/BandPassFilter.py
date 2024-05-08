from scipy import signal
import numpy as np
def BandPassFilter(Data_in, Fdominant, ddF, fs):
    
    
    dF = ddF * Fdominant  # band around dominant mode
    Fstop1 = Fdominant - 2 * dF if Fdominant - 2 * dF > 0.01 else 0.01
    Fpass1 = Fdominant - dF if Fdominant - dF > 0.01 else 0.03
    Fpass2 = Fdominant + dF
    Fstop2 = Fdominant + 2 * dF
    Astop1 = 10  
    Apass = 1  
    Astop2 = 10 
    b, a = signal.iirdesign(wp=[Fpass1, Fpass2], ws=[Fstop1, Fstop2],
                         gpass=Apass, gstop=Astop1, fs=fs, analog=False,
                         ftype='butter')

    # Apply the filter to the data
    Data_out = signal.filtfilt(b, a, Data_in)
    return Data_out.T