"""
Detector analysis utilities for radlabpy.

This subpackage provides basic tools for detector efficiency, event
rates, coincidence analysis and signal-to-noise calculations.
"""

from .coincidence import accidental_coincidence_rate, coincidence_rate
from .efficiency import detection_efficiency, efficiency_uncertainty
from .rates import event_rate, rate_uncertainty
from .signals import signal_to_noise

__all__ = [
    "detection_efficiency",
    "efficiency_uncertainty",
    "event_rate",
    "rate_uncertainty",
    "coincidence_rate",
    "accidental_coincidence_rate",
    "signal_to_noise",
]