"""
Coincidence analysis utilities.

This module provides basic tools to calculate coincidence rates and
accidental coincidence rates for simple two-channel detector systems.

Conventions
-----------
The coincidence rate is defined as:

    coincidence_rate = coincidences / time

For two independent channels and a symmetric coincidence time window,
the accidental coincidence rate is approximated as:

    R_acc = 2 * rate1 * rate2 * coincidence_window
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

def coincidence_rate(coincidences, time):
    """
    Calculate the coincidence rate.

    The coincidence rate is defined as:

        coincidence_rate = coincidences / time

    Parameters
    ----------
    coincidences : float, int, list, tuple, or array-like
        Number of coincidence events. Must be non-negative.
    time : float, int, list, tuple, or array-like
        Measurement time. Must be greater than zero.

    Returns
    -------
    float or numpy.ndarray
        Coincidence rate in coincidences per unit time.

    Notes
    -----
    If time is given in seconds, the returned rate is in coincidences
    per second.
    """    
    coincidences_array = _as_array(coincidences, name="coincidences")
    time_array = _as_array(time, name="time")

    _validate_finite(coincidences_array, name="coincidences")
    _validate_finite(time_array, name="time")   

    if np.any(coincidences_array < 0):
        raise ValueError("coincidence must be non-negative.")

    if np.any(time_array <= 0):
        raise ValueError("time must be greater than zero.")

    result = coincidences_array / time_array

    return _return_sacalar_if_scalar(result)

def accidental_coincidence_rate(rate1, rate2, coincidence_window):
    """
    Estimate the accidental coincidence rate for two independent channels.

    The accidental coincidence rate is approximated as:

        R_acc = 2 * rate1 * rate2 * coincidence_window

    Parameters
    ----------
    rate1 : float, int, list, tuple, or array-like
        Event rate of the first detector channel. Must be non-negative.
    rate2 : float, int, list, tuple, or array-like
        Event rate of the second detector channel. Must be non-negative.
    coincidence_window : float, int, list, tuple, or array-like
        Symmetric coincidence time window. Must be greater than zero.

    Returns
    -------
    float or numpy.ndarray
        Accidental coincidence rate.

    Raises
    ------
    ValueError
        If any rate is negative, the coincidence window is not positive,
        or inputs contain non-finite values.

    Notes
    -----
    This simple approximation assumes two independent channels and a
    symmetric coincidence window. If rates are in Hz and the window is in
    seconds, the accidental rate is returned in Hz.
    """    
    rate1_array = _as_array(rate1, name="rate1")
    rate2_array = _as_array(rate2, name="rate2")
    window_array = _as_array(coincidence_window, name="coincidence_window")

    _validate_finite(rate1_array, name="rate1")
    _validate_finite(rate2_array, name="rate2")
    _validate_finite(window_array, name="coincidence_window")   

    if np.any(rate1_array < 0):
        raise ValueError("rate1 must be non-negative.")

    if np.any(rate2_array < 0):
        raise ValueError("rate2 must be non-negative.")

    if np.any(window_array <= 0):
        raise ValueError("coincidence_window must be greater than zero.")
    
    result = 2.0 * rate1_array * rate2_array * window_array

    return _return_sacalar_if_scalar(result)

