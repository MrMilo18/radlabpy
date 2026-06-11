"""
Event rate utilities for detector analysis.

This module provides basic tools to calculate event rates and their
Poisson statistical uncertainties.

Conventions
-----------
The event rate is defined as:

    rate = counts / time

where ``counts`` is the number of observed events and ``time`` is the
measurement time.

For Poisson counting statistics, the statistical uncertainty is:

    sigma_rate = sqrt(counts) / time
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

def _validate_rate_inputs(counts, time):
    """
    Validate counts and measurement time.

    Parameters
    ----------
    counts : float, int, list, tuple, or array-like
        Number of counted events.
    time : float, int, list, tuple, or array-like
        Measurement time.

    Returns
    -------
    tuple of numpy.ndarray
        Validated counts and time arrays.
    """    
    counts_array = _as_array(counts, name="counts")
    time_array = _as_array(time, name="time")

    _validate_finite(counts_array, name="counts")
    _validate_finite(time_array, name="time")   

    if np.any(counts_array < 0):
        raise ValueError("counts must be non-negative")
    
    if np.any(time_array <= 0 ):
        raise ValueError("time must be greater than zero.")
    
    return counts_array, time_array

def event_rate(counts, time):
    """
    Calculate the event rate.

    The event rate is defined as:

        rate = counts / time

    Parameters
    ----------
    counts : float, int, list, tuple, or array-like
        Number of counted events. Must be non-negative.
    time : float, int, list, tuple, or array-like
        Measurement time. Must be greater than zero.

    Returns
    -------
    float or numpy.ndarray
        Event rate in counts per unit time.

    Raises
    ------
    ValueError
        If counts is negative, time is not positive, or inputs contain
        non-finite values.

    Notes
    -----
    If time is given in seconds, the returned rate is in counts per second.
    If time is given in minutes, the returned rate is in counts per minute.
    """
    counts_array, time_array = _validate_rate_inputs(counts, time)

    result = counts_array / time_array

    return _return_sacalar_if_scalar(result)

def rate_uncertainty(counts, time):
    """
    Calculate the Poisson statistical uncertainty of an event rate.

    The rate uncertainty is calculated as:

        sigma_rate = sqrt(counts) / time

    Parameters
    ----------
    counts : float, int, list, tuple, or array-like
        Number of counted events. Must be non-negative.
    time : float, int, list, tuple, or array-like
        Measurement time. Must be greater than zero.

    Returns
    -------
    float or numpy.ndarray
        Statistical uncertainty of the event rate.

    Notes
    -----
    The formula assumes Poisson counting statistics.
    """
    counts_array, time_array = _validate_rate_inputs(counts, time)

    result = np.sqrt(counts_array) / time_array

    return _return_sacalar_if_scalar(result)       
