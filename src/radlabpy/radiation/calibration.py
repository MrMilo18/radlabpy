"""
Energy calibration utilities for radiation spectra.

This module provides basic tools for linear channel-energy calibration.

The calibration convention used here is:

    E = slope * channel + intercept

where E is the energy and channel is the detector channel number.
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
        return np.asanyarray(values, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must contain numeric values.") from exc

def _validate_finite(values, name:str = "values") -> None:
    """
    Validate that all values are finite numbers.
    """

    array = _as_array(values, name=name)

    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values.")
    
def _validate_calibration_points(channels, energies):
    """
    Validate channel and energy arrays for linear calibration.
    """

    channels_array = _as_array(channels, name="channels")
    energies_array = _as_array(energies, name="energies")

    if channels_array.size == 0:
        raise ValueError("channels must be not empty.")
    if energies_array.size == 0:
        raise ValueError("energies must be not empty.")
    
    if channels_array.shape != energies_array.shape:
        raise ValueError("channels and energies must have the samen shape.")
    
    if channels_array.size < 2:
        raise ValueError("At least two calibration points are required.")
    
    _validate_finite(channels_array, name="channels")
    _validate_finite(energies_array, name="energies")

    if np.allclose(channels_array, channels_array.flat[0]):
        raise ValueError("channels must contain at least two distinct values.")

    return channels_array, energies_array

def _validate_calibration(calibration):
    """
    Validate a calibration dictionary.
    """

    if not isinstance(calibration, dict):
        raise ValueError("calibration must be a dictionary.")
    
    if "slope" not in calibration:
        raise ValueError("calibration must contain 'slope'.")
    if "intercept" not in calibration:
        raise ValueError("calibration must contain 'intercept'.")
    
    try:
        slope = float(calibration["slope"])
        intercept = float(calibration["intercept"])
    except (TypeError, ValueError) as exc:
        raise ValueError("calibration parameters must be numeric.") from exc
    
    if not np.isfinite(slope):
        raise ValueError("calibration slope must be finite.")
    if not np.isfinite(intercept):
        raise ValueError("calibration intercept must be finite.")
    
    if np.isclose(slope, 0.0):
        raise ValueError("calibration slope must not be zero.")
    
    return slope, intercept

def linear_calibration(channels, energies) -> dict[str, float]:
    """
    Fit a linear channel-energy calibration.

    The calibration convention is:

        E = slope * channel + intercept

    Parameters
    ----------
    channels : array-like
        Detector channel values.
    energies : array-like
        Known energies associated with each channel.

    Returns
    -------
    dict
        Dictionary containing:

        - slope
        - intercept
        - r_value
        - r_squared

    Raises
    ------
    ValueError
        If inputs are empty, non-numeric, non-finite, have different
        shapes, contain fewer than two points, or produce a zero slope.
    """
    channels_array, enrgies_array = _validate_calibration_points(channels, energies)

    slope, intercept = np.polyfit(channels_array, enrgies_array, deg=1)

    if np.isclose(slope, 0.0):
        raise ValueError(
            "Calibration slope is zero or numerizally close to zero."
            "Energy must vary with channel."
        )  

    r_matrix = np.corrcoef(channels_array, enrgies_array)
    r_value = float(r_matrix[0, 1])
    r_squared = float(r_value**2)

    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "r_value": r_value,
        "r_squared": r_squared,
    }  

def channel_to_energy(channels, calibration):
    """
    Convert detector channels to energy using a linear calibration.

    Parameters
    ----------
    channels : float, int, list, tuple, or array-like
        Channel value or values.
    calibration : dict
        Calibration dictionary returned by ``linear_calibration``.

    Returns
    -------
    float or numpy.ndarray
        Energy value or values.
    """
    slope, intercept = _validate_calibration(calibration)

    channels_array = _as_array(channels, name="channels")
    _validate_finite(channels_array, name="channels")

    result = slope * channels_array + intercept

    if np.isscalar(channels):
        return float(result)

    return result

def energy_to_channel(energies, calibration):
    """
    Convert energies to detector channels using a linear calibration.

    Parameters
    ----------
    energies : float, int, list, tuple, or array-like
        Energy value or values.
    calibration : dict
        Calibration dictionary returned by ``linear_calibration``.

    Returns
    -------
    float or numpy.ndarray
        Channel value or values.
    """ 
    slope, intercept = _validate_calibration(calibration)

    energies_array = _as_array(energies, name="energies")
    _validate_finite(energies_array, name="energies")

    result = (energies_array - intercept) / slope

    if np.isscalar(energies):
        return float(result)
    
    return result

def calibration_residuals(channels, energies, calibration):
    """
    Calculate residuals for a linear channel-energy calibration.

    Residuals are defined as:

        residual = observed_energy - calibrated_energy

    Parameters
    ----------
    channels : array-like
        Detector channel values.
    energies : array-like
        Known or observed energy values.
    calibration : dict
        Calibration dictionary returned by ``linear_calibration``.

    Returns
    -------
    numpy.ndarray
        Residuals between observed energies and calibrated energies.
    """
    channels_array, energies_array = _validate_calibration_points(channels, energies)
    calibrated_energies = channel_to_energy(channels_array, calibration)

    return energies_array - calibrated_energies
  