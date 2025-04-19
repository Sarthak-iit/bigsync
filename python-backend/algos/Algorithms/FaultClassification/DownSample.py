import numpy as np

def downsample_array(arr, fraction=0.2):
    """
    Downsamples a 1D array by selecting points at equal intervals.

    Parameters:
        arr (np.ndarray or list): Input data (1D array or list)
        fraction (float): Fraction of data to retain (default 0.2 for 20%)

    Returns:
        np.ndarray: Downsampled data points
    """
    arr = np.asarray(arr)  # Ensure input is a NumPy array
    num_points = int(len(arr) * fraction)  # Calculate target size
    if num_points < 1:
        return arr  # If too few points, return original array
    
    step = max(len(arr) // num_points, 1)  # Ensure step is at least 1
    return arr[::step][:num_points]  # Select data at equal intervals