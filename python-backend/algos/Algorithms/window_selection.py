import numpy as np
from scipy.signal import find_peaks
from scipy.linalg import toeplitz

# isStable = None
def findEnvelopeAndNatureOfMode(data):
    data = data.flatten()
    peaks, _ = find_peaks(data)
    if len(peaks) == 0:
        return data[0] < data[-1]
    # isStable = np.sum(np.gradient(data[peaks].flatten())) < 0
    try:
        isStable = np.sum(np.gradient(data[peaks].flatten())) < 0
    except:
        isStable = data[peaks][0] < 0
    # return isStable
    return isStable

def findMonotonicSections(IE,isStable):
    sections = []
    if not isStable:
        i = 0
        while(i < len(IE)-1):
            curr = []
            while  i < len(IE)-1 and IE[i+1] - IE[i] > 0 :
                curr.append(i)
                i += 1
            i+= 1
            if len(curr)>0: sections.append(curr)
    else:
        i = 0
        while(i < len(IE)-1):
            curr = []
            while i < len(IE)-1 and IE[i+1] - IE[i] < 0:
                curr.append(i)
                i += 1
            i+= 1
            if len(curr)>0: sections.append(curr)

        
    return sections

def findConstantSections(no_of_samples_by_user, IF,threshold):
    window_size = 2*no_of_samples_by_user
    stable_indices = []
    
    for i in range(len(IF) - window_size):
        if np.std(IF[i:i+window_size]) < threshold:
            stable_indices += list(np.arange(i, i+window_size))
    
    return stable_indices

def findCommonIndices(sections, stable_indices):
    common_indices = []
    for section in sections:
        temp = np.intersect1d(stable_indices, section)#culprit for slowing the application
        if len(temp) > 0 :
            for t in temp: common_indices.append(t)
    return common_indices

def finalChosenArea(common_indices):
    no_of_samples_by_user = 70
    median_common_indices = common_indices[len(common_indices)//2]
    chosen_start = median_common_indices - no_of_samples_by_user//2
    chosen_end = median_common_indices + no_of_samples_by_user//2
    return[chosen_start, chosen_end]


def windowSelection(data,IE,IF):
    data = np.array(data)
    isStable = findEnvelopeAndNatureOfMode(data)
    sections = findMonotonicSections(IE,isStable)
    stable_indices = findConstantSections(100, IF, 0.05)
    common_indices = findCommonIndices(sections, stable_indices)
    if len(common_indices) == 0:
        return []
    [chosen_start, chosen_end] = finalChosenArea(common_indices)
    return data[chosen_start:chosen_end]

        