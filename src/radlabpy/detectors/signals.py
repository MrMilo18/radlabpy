"""
Signal utilities for detector analysis.

This module provides simple tools for detector signal analysis, such as
the signal-to-noise ratio.
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

def signal_to_noise(signal, noise):
    """
    Calculate the signal-to-noise ratio.

    The signal-to-noise ratio is defined as:

        SNR = signal / noise

    Parameters
    ----------
    signal : float, int, list, tuple, or array-like
        Signal amplitude, signal counts, or signal rate.
    noise : float, int, list, tuple, or array-like
        Noise amplitude, noise counts, or noise rate. Must be greater
        than zero.

    Returns
    -------
    float or numpy.ndarray
        Signal-to-noise ratio. It is dimensionless when signal and noise
        are expressed in the same units.

    Notes
    -----
    This function does not subtract background. It only computes the ratio
    between a provided signal value and a provided noise value.
    """
    signal_array = _as_array(signal, name="signal")
    noise_array = _as_array(noise, name="noise")

    _validate_finite(signal_array, name="signal")
    _validate_finite(noise_array, name="noise")

    if np.any(noise_array <= 0):
        raise ValueError("noise must be greater than zero.")

    result = signal_array / noise_array

    return _return_sacalar_if_scalar(result)