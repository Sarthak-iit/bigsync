import math
import numpy as np
from algos.Algorithms.OSLP.denoise import denoiseSignal



def calculate_power(voltages, voltage_angles, currents, current_angles):
    # voltage_angles = np.unwrap(voltage_angles)
    # current_angles = np.unwrap(current_angles
    voltages = np.array(voltages)*1000
    voltage_angles = np.array(voltage_angles)

    currents= np.array(currents)
    current_angles = np.array(current_angles)   

    # angle_diff = (voltage_angles - current_angles)/180*np.pi
    angle_diff = np.unwrap((voltage_angles - current_angles)/180*np.pi)
    real_power = math.sqrt(3)*voltages * currents * np.cos(angle_diff)
    reactive_power = math.sqrt(3)*voltages * currents * np.sin(angle_diff)
    return real_power, reactive_power


def LineFlowCalculation(vm, va, im, ia):
    ia = np.unwrap(np.array(ia))
    va = np.unwrap(np.array(va))
    im = np.array(im)
    vm = np.array(vm)*1000
    U = vm * np.exp(1j * va / 180 * np.pi)
    I = im * np.exp(1j * ia / 180 * np.pi)
    S = U * np.conj(I)
    P = np.real(S)
    Q = np.imag(S)
    P = denoiseSignal(P)
    Q = denoiseSignal(Q)
    return P, Q
