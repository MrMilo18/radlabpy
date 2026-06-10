"""
Radiation analysis tools.

This subpackage contains functions for radiation counting statistics,
spectral analysis, calibration, and related utilities.
"""


from .counting import (
    poisson_uncertainty,
    counting_summary,
    count_rate,
    cps_to_cpm,
    cpm_to_cps,
)

from .fitting import(
    gaussian,
    fwhm_from_sigma,
    energy_resolution,
    estimate_peak_area,
    fit_gaussian_peak,
)

from .spectra import(
    total_counts,
    normalize_spectrum,
    find_peak_channel,
)

__all__ = [
    "counting_summary",
    "count_rate",
    "cpm_to_cps",
    "cps_to_cpm",
    "poisson_uncertainty",
    "energy_resolution",
    "estimate_peak_area",
    "fit_gaussian_peak",
    "fwhm_from_sigma",
    "gaussian",
    "find_peak_channel",
    "normalize_spectrum",
    "total_counts",
]