"""
Detector efficiency utilities.

This module provides basic functions to compute detection efficiency
and its approximate binomial statistical uncertainty.

Conventions
-----------
Efficiency is defined as

    efficiency = detected / emitted

where ``detected`` is the number of detected events and ``emitted`` is
the number of emitted or expected events.

The approximate binomial uncertainty is

    sigma_eff = sqrt(efficiency * (1 - efficiency) / emitted)
"""

from __future__ import annotations

import numpy as np

def _as_array(values, name: str = "values"):
    """
    Convert input values to a NumPy array with float dtype.

    Parameters
    ----------
    values : float, int, list, tuple, or array-like
        Input numerical values.
    name : str
        Name used in error messages.
    """
    try:
        return np.asarray(values, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must contain numeric values.") from exc
    
def _validate_finite(values, name:str = "values") -> None:
    """
    Validate that all values are finite numbers.

    Parameters
    ----------
    values : array-like
        Values to validate.
    name : str
        Name used in error messages.

    """

    array = _as_array(values, name=name)

    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values.")

def _return_sacalar_if_scalar(result):
    """
    Return a Python float if the result is scalar-like.

    Otherwise, return the NumPy array.
    """
    result = np.asarray(result, dtype=float)

    if result.ndim == 0:
        return float(result)
    
    return result

def _validate_effiency_inputs(detected, emitted):
    """
    Validate detected and emitted event counts.

    Parameters
    ----------
    detected : float, int, list, tuple, or array-like
        Number of detected events.
    emitted : float, int, list, tuple, or array-like
        Number of emitted, generated or expected events.

    Return
    ------
    tuple of numpy.ndarray
        Validated detected and emitted arrays.
    
    """

    detected_array = _as_array(detected, name="detected")
    emitted_array = _as_array(emitted, name="emitted")

    _validate_finite(detected_array, name="detected")
    _validate_finite(emitted_array, name="emitted")

    if np.any(detected_array < 0):
        raise ValueError("detected must be non-negative.")

    if np.any(emitted_array <= 0):
        raise ValueError("emitted must be grater than zero.")
    
    if np.any(detected_array > emitted_array):
        raise ValueError("detected cannot be grater than emitted.")
    
    return detected_array, emitted_array

def detection_efficiency(detected, emitted):
    """
    Calculate the detection efficiency.

    The efficiency is defined as:

        efficiency = detected / emitted

    Parameters
    ----------
    detected : float, int, list, tuple, or array-like
        Number of detected events. Must be non-negative.
    emitted : float, int, list, tuple, or array-like
        Number of emitted, generated or expected events. Must be greater
        than zero.

    Returns
    -------
    float or numpy.ndarray
        Detection efficiency. The result is dimensionless.  

    Notes
    -----
    Scalar inputs return a Python float. Array-like inputs return a
    NumPy array. 
    """

    detected_array, emitted_array = _validate_effiency_inputs(detected, emitted)

    result = detected_array / emitted_array

    return _return_sacalar_if_scalar(result)

def efficiency_uncertainty(detected, emitted):
    """
    Calculate the approximate binomial uncertainty of the efficiency.

    The uncertainty is calculated as:

        sigma_eff = sqrt(efficiency * (1 - efficiency) / emitted)

    Parameters
    ----------
    detected : float, int, list, tuple, or array-like
        Number of detected events. Must be non-negative.
    emitted : float, int, list, tuple, or array-like
        Number of emitted, generated or expected events. Must be greater
        than zero.

    Returns
    -------
    float or numpy.ndarray
        Approximate binomial statistical uncertainty of the efficiency.


    Notes
    -----
    This uncertainty is statistical only. It does not include systematic
    uncertainties from detector calibration, source activity, geometry,
    dead time or background subtraction.    
    """
    detection_array, emitted_array = _validate_effiency_inputs(detected, emitted)

    efficiency = detection_array / emitted_array
    result = np.sqrt(efficiency * (1.0 - efficiency) / emitted_array)

    return _return_sacalar_if_scalar(result)


