"""
Convenient operations

"""

import numpy as np
import scipy.integrate as integrate
from scipy.constants import elementary_charge as ECHARGE

IMPEDANCE = 50

def average_wf(waveforms):
    """
    Get the average waveform

    Args:
        waveforms (list):

    Returns:
        np.ndarray
    """
    wf0 = waveforms[0]
    for wf in waveforms[1:]:
        wf0 += wf

    return wf0 / float(len(waveforms))

def integrate_wf(header, waveform, method=integrate.simps):
    """
    Integrate a waveform to get the total charge

    Args:
        header (dict):
        waveform (np.ndarray):

    Returns:
        float
    """
    integral = method(waveform, header["xs"], header["xincr"])
    return integral

def calculate_gain(header, waveform):
    """
    Calculate the gain of a PMT

    Args:
        header (dict):
        waveform (np.ndarray):

    Returns:
        float
    """

    charge = abs(integrate_wf(header, waveform/IMPEDANCE))
    return charge/ECHARGE

def save_waveform(header, waveform, filename):
    """
    save a waveform together with its header

    Args:
        header (dict):
        waveform (np.ndarray):
        filename (str):
    Returns:
        None
    """
    np.save((head, waveform), filename)
    return None


def load_waveform(filenaame):
    """
    load a waveform from a file

    Args:
        filenaame (str): 

    Returns:
        dict
    """
    head, wf = np.load(filename)