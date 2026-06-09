"""
Radiation analysis tools.

This subpackage contains functions for radiation counting statistics,
spectral analysis, calibration, and related utilities.
"""

__version__ = "0.1.0"

from .counting import (
    poisson_uncertainty,
    counting_summary,
    count_rate,
    cps_to_cpm,
    cpm_to_cps,
)

__all__ = [
    "poisson_uncertainty",
    "counting_summary",
    "count_rate",
    "cps_to_cpm",
    "cpm_to_cps",
]