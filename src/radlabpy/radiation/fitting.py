"""Gaussian fitting utilities for radiation spectra.

This module contains numerical tools for simple spectral peak analysis:
Gaussian peak evaluation, FWHM calculation, relative energy resolution,
peak area estimation, and basic Gaussian peak fitting.

The functions here are intended to contain calculation logic only.
Plotting should be handled in examples or in a separate plotting module.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import curve_fit

def gaussian(
        x: float | np.array,
        amplitude: float,
        mean: float,
        sigma: float,
        background: float = 0,
)  -> float | np.ndarray:
    """Evaluate a Gaussian function with a constant background.

    The function is defined as:

        y = amplitude * exp(-(x - mean)^2 / (2 sigma^2)) + background

    Parameters
    ----------
    x : float or numpy.ndarray
        Position or array of positions where the Gaussian is evaluated.
    amplitude : float
        Peak amplitude above background.
    mean : float
        Gaussian mean or peak center.
    sigma : float
        Gaussian standard deviation. It must be positive.
    background : float, optional
        Constant background added to the Gaussian. Default is 0.

    Returns
    -------
    float or numpy.ndarray
        Gaussian value evaluated at ``x``.

    Raises
    ------
    ValueError
        If ``sigma`` is not positive.
    """

    if sigma <= 0:
        raise ValueError("Sigma must be positive.")
    
    x_array = np.asanyarray(x, dtype=float)
    values = amplitude * np.exp(-0.5 * ((x_array - mean) / sigma) ** 2) + background

    if np.isscalar(x):
        return float(values)
    
    return values

def fwhm_from_sigma(sigma: float) -> float:
    """Calculate the full width at half maximum of a Gaussian peak.

    Parameters
    ----------
    sigma : float
        Standard deviation of the Gaussian peak. It must be positive.
        The unit is the same as the x-axis unit, for example channels or keV.

    Returns
    -------
    float
        Full width at half maximum, in the same unit as ``sigma``.

    Raises
    ------
    ValueError
        If ``sigma`` is not positive.
    """
    if sigma <= 0: 
        raise ValueError("sigma must be positive.")
    
    return 2.0 * np.sqrt(2.0 * np.log(2.0)) * sigma

def energy_resolution(fwhm: float, energy: float) -> float:
    """Calculate relative energy resolution.

    The relative energy resolution is defined as

        R = FWHM / E.

    Parameters
    ----------
    fwhm : float
        Full width at half maximum.
    energy : float
        Peak energy or centroid value.

    Returns
    -------
    float
        Relative energy resolution.

    Raises
    ------
    ValueError
        If `fwhm` is negative or if `energy` is not positive.
    """
    if fwhm < 0:
        raise ValueError("fwhm must be non-negative.")
    if energy <= 0:
        raise ValueError("energy must be positive.")

    return fwhm / energy

def estimate_peak_area(amplitude: float, sigma: float) -> float:
    """Estimate the area under a Gaussian peak.

    For a Gaussian peak without background,

        area = amplitude * sigma * sqrt(2*pi).

    Parameters
    ----------
    amplitude : float
        Peak amplitude.
    sigma : float
        Standard deviation of the Gaussian peak.

    Returns
    -------
    float
        Estimated peak area.

    Raises
    ------
    ValueError
        If `amplitude` is negative or if `sigma` is not positive.
    """
    if amplitude < 0 :
        raise ValueError("Amplitude must be non-negative.")
    if sigma <= 0:
        raise ValueError("Sigma must be positive.")
    
    return amplitude * sigma * np.sqrt(2.0 * np.pi)

def fit_gaussian_peak(x,y) -> dict[str, float]:
    """Fit a Gaussian peak with constant background.

    Parameters
    ----------
    x : array-like
        Channel or energy values.
    y : array-like
        Counts associated with each `x` value.

    Returns
    -------
    dict
        Dictionary containing the fitted parameters:

        - amplitude
        - mean
        - sigma
        - background

    Raises
    ------
    ValueError
        If `x` and `y` do not have the same shape, contain too few points,
        or if the input data are not suitable for fitting.
    RuntimeError
        If the fit does not converge.
    """

    x_array = np.array(x, dtype=float)
    y_array = np.array(y, dtype=float)

    if x_array.shape != y_array.shape:
        raise ValueError("x and y must have same shape.")   
    if x_array.size < 4:
        raise ValueError("At least four data points are required for fitting.")
    if not np.all(np.isfinite(x_array)) or not np.all(np.isfinite(y_array)):
        raise ValueError("x and y must contain only finite values.")

    background_guess = float(np.min(y_array))
    amplitude_guess = float(np.max(y_array) - background_guess)
    mean_guess = float(x_array[np.argmax(y_array)]) 

    if amplitude_guess <= 0:
        raise ValueError("cannot estimate a positive peak amplitude from the data.")
    
    weights = y_array - background_guess
    weights = np.clip(weights, a_min=0.0, a_max = None)

    if np.sum(weights) > 0:
        variance_guess = np.sum(weights * (x_array - mean_guess) ** 2) / np.sum(weights)
        sigma_guess = float(np.sqrt(variance_guess))
    else:
        sigma_guess = float((np.max(x_array) - np.min(x_array)) / 10.0)

    initial_guess = [
        amplitude_guess,
        mean_guess,
        sigma_guess,
        background_guess,
    ]

    lower_bounds = [0.0, np.min(x_array), 1e-12, -np.inf]
    upper_bounds = [np.inf, np.max(x_array), np.inf, np.inf]

    popt, _ = curve_fit(
        gaussian,
        x_array,
        y_array,
        p0=initial_guess,
        bounds=(lower_bounds, upper_bounds),
        maxfev = 10000,
    )

    amplitude, mean, sigma, background = popt

    return {
        "amplitude": float(amplitude),
        "mean": float(mean),
        "sigma": float(abs(sigma)),
        "background": float(background),
    }