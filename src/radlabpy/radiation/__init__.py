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

from .calibration import(
    linear_calibration,
    channel_to_energy,
    energy_to_channel,
    calibration_residuals,
)

__all__ = [
    "poisson_uncertainty",
    "counting_summary",
    "count_rate",
    "cps_to_cpm",
    "cpm_to_cps",
    "gaussian",
    "fwhm_from_sigma",
    "energy_resolution",
    "estimate_peak_area",
    "fit_gaussian_peak",
    "total_counts",
    "normalize_spectrum",
    "find_peak_channel",
    "linear_calibration",
    "channel_to_energy",
    "energy_to_channel",
    "calibration_residuals",
]