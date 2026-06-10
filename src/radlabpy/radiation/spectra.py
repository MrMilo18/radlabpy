"""Basic spectrum utilities for radiation analysis."""

from __future__ import annotations

import numpy as np

def total_counts(counts) -> float:
    """Calculate total counts in a spectrum.

    Parameters
    ----------
    counts : array-like
        Spectrum counts.

    Returns
    -------
    float
        Sum of all counts.

    Raises
    ------
    ValueError
        If `counts` is empty, contains non-finite values, or contains
        negative values.
    """

    counts_array = np.asarray(counts, dtype=float)

    if counts_array.size == 0:
        raise ValueError("counts must not be empty.")
    if not np.all(np.isfinite(counts_array)):
        raise ValueError("counts must contain only finite values.")    
    if np.any(counts_array < 0):
        raise ValueError("counts must be non-negative.")
    
    return float(np.sum(counts_array))


def normalize_spectrum(counts):
    """Normalize a spectrum by its total counts.

    Parameters
    ----------
    counts : array-like
        Spectrum counts.

    Returns
    -------
    numpy.ndarray
        Normalized spectrum whose sum is 1.

    Raises
    ------
    ValueError
        If the total number of counts is zero.
    """

    counts_array = np.asarray(counts, dtype=float)
    total = total_counts(counts_array)

    if total <= 0:
        raise ValueError("cannot normalize a spectrum with zero total counts.") 

    return counts_array / total

def find_peak_channel(channels, counts):
    """Find the channel corresponding to the maximum count.

    Parameters
    ----------
    channels : array-like
        Channel values.
    counts : array-like
        Spectrum counts.

    Returns
    -------
    float
        Channel value where the spectrum reaches its maximum.

    Raises
    ------
    ValueError
        If `channels` and `counts` do not have the same shape or are empty.
    """    

    channels_array = np.asarray(channels, dtype=float)
    counts_array = np.asarray(counts, dtype=float)

    if channels_array.shape != counts_array.shape:
        raise ValueError("channels and counts must have the same shape.")
    if channels_array.size == 0:
        raise ValueError("channels and counts must not be empty.")
    if not np.all(np.isfinite(channels_array)) or not np.all(np.isfinite(counts_array)):
        raise ValueError("channels and counts must contain only finite values.")
    if np.any(counts_array < 0):
        raise ValueError("counts must be non-negative.")

    peak_index = int(np.argmax(counts_array))
    return float(channels_array[peak_index]) 

