"""
Counting statistics utilities for radiation measurements.

This module provides basic tools for radiation counting analysis,
including Poisson uncertainties, count rates, and CPS/CPM conversions.

The functions are designed to be small, testable, and reusable.
"""

from __future__ import annotations

import numpy as np

def _as_array(values):
    """
    Convert input values to a NumPy array with float dtype

    Parameters
    ----------
    values : float, int, list, tuple, or array-like
        Input numerical values.
    """
    return np.asanyarray(values, dtype=float)


def _validate_non_negative(values, name: str = "values") -> None:
    """
    Validate that all values are non-negative
    """

    array = _as_array(values)

    if np.any(array < 0):
        raise ValueError(f"{name} must be non-negative.")
    

def poisson_uncertainty(counts):
    """
    Compute the Poisson statistical uncertainty of radiation counts.

    For Poisson-distributed counts, the standard uncertainty is

        sigma_N = sqrt(N)

    Parameters
    ----------
    counts : float, int, list, tuple, or array-like
        Number of counts. Counts must be non-negative.

    Returns
    -------
    float or numpy.ndarray
        Poisson uncertainty associated with the input counts.

    Raises
    ------
    ValueError
        If any count is negative.

    Examples
    --------
    >>> poisson_uncertainty(100)
    10.0
    """
    _validate_non_negative(counts, name="counts")

    counts_array = _as_array(counts)
    result = np.sqrt(counts_array)

    if np.isscalar(counts):
        return float(result)

    return result

def counting_summary(counts):
    """
    Compute a statistical summary of radiation count measurements.

    Parameters
    ----------
    counts : list, tuple, or array-like
        Sequence of count measurements. Counts must be non-negative.

    Returns
    -------
    dict
        Dictionary containing:
        - n_measurements
        - total_counts
        - mean_counts
        - std_counts
        - min_counts
        - max_counts
        - poisson_uncertainty_mean

    Raises
    ------
    ValueError
        If counts is empty or contains negative values.
    """

    counts_array = _as_array(counts)

    if counts_array.size == 0:
        raise ValueError("Counts must not be empty")
    
    _validate_non_negative(counts_array, name="counts")

    mean_counts = np.mean(counts_array)

    return {
        "n_measurements": int(counts_array.size),
        "total_counts": float(np.sum(counts_array)),
        "mean_counts": float(mean_counts),
        "std_counts": float(np.std(counts_array, ddof=1)) if counts_array.size > 1 else 0.0,
        "min_counts": float(np.min(counts_array)),
        "max_counts": float(np.max(counts_array)),
        "poisson_uncertainty_mean": float(np.sqrt(mean_counts)),
    }

def count_rate(counts, time):

    _validate_non_negative(counts, name="counts")

    counts_array = _as_array(counts)
    time_array = _as_array(time)

    if np.any(time_array <= 0):
        raise ValueError("Time must be positive")
    
    result = counts_array / time_array

    if np.isscalar(counts) and np.isscalar(time):
        return float(result)
    
    return result

def cps_to_cpm(cps):
    """
    Convert counts per second to counts per minute

    Parameters
    ----------
    cps : float, int, list, tuple, or array-like
        Count rate in counts per second. Values must be non-negative.

    """
    _validate_non_negative(cps, name="cps")
    cps_array = _as_array(cps)
    result = cps_array * 60

    if np.isscalar(cps):
        return float(result)
    
    return result

def cpm_to_cps(cpm):
    """
    Convert counts per minute to counts per second

    Parameters
    ----------
    cps : float, int, list, tuple, or array-like
        Count rate in counts per second. Values must be non-negative.

    """
    _validate_non_negative(cpm, name="cpm")
    cpm_array = _as_array(cpm)
    result = cpm_array / 60

    if np.isscalar(cpm):
        return float(result)
    
    return result

