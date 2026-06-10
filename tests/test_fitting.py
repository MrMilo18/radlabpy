"""Unit tests for Gaussian fitting utilities."""

import math

import numpy as np
import pytest

from radlabpy.radiation import (
    energy_resolution,
    estimate_peak_area,
    fit_gaussian_peak,
    fwhm_from_sigma,
    gaussian,
)


def test_fwhm_from_sigma_known_value():
    """FWHM for sigma = 1 should be approximately 2.3548."""
    result = fwhm_from_sigma(1.0)

    assert math.isclose(result, 2.3548, rel_tol=1e-4)


def test_fwhm_from_sigma_invalid_sigma():
    """sigma <= 0 should raise ValueError."""
    with pytest.raises(ValueError):
        fwhm_from_sigma(0.0)

    with pytest.raises(ValueError):
        fwhm_from_sigma(-1.0)


def test_energy_resolution_known_value():
    """Energy resolution should be FWHM divided by energy."""
    result = energy_resolution(2.0, 100.0)

    assert math.isclose(result, 0.02, rel_tol=1e-12)


def test_energy_resolution_invalid_energy():
    """energy <= 0 should raise ValueError."""
    with pytest.raises(ValueError):
        energy_resolution(2.0, 0.0)

    with pytest.raises(ValueError):
        energy_resolution(2.0, -100.0)


def test_gaussian_at_mean():
    """At x = mean, Gaussian value should be amplitude + background."""
    amplitude = 100.0
    mean = 50.0
    sigma = 3.0
    background = 10.0

    result = gaussian(mean, amplitude, mean, sigma, background)

    assert math.isclose(result, amplitude + background, rel_tol=1e-12)


def test_gaussian_invalid_sigma():
    """sigma <= 0 should raise ValueError."""
    with pytest.raises(ValueError):
        gaussian(1.0, amplitude=10.0, mean=0.0, sigma=0.0)


def test_estimate_peak_area_positive():
    """Peak area should be positive for positive amplitude and sigma."""
    area = estimate_peak_area(amplitude=100.0, sigma=2.0)

    assert area > 0.0


def test_estimate_peak_area_invalid_sigma():
    """sigma <= 0 should raise ValueError."""
    with pytest.raises(ValueError):
        estimate_peak_area(amplitude=100.0, sigma=0.0)


def test_estimate_peak_area_invalid_amplitude():
    """Negative amplitude should raise ValueError."""
    with pytest.raises(ValueError):
        estimate_peak_area(amplitude=-1.0, sigma=1.0)


def test_fit_gaussian_peak_recovers_mean():
    """Gaussian fit should recover the mean from synthetic data."""
    expected_mean = 42.0

    x = np.linspace(0.0, 100.0, 301)
    y = gaussian(
        x,
        amplitude=150.0,
        mean=expected_mean,
        sigma=5.0,
        background=12.0,
    )

    fit = fit_gaussian_peak(x, y)

    assert math.isclose(fit["mean"], expected_mean, abs_tol=0.5)


def test_fit_gaussian_peak_invalid_shapes():
    """x and y must have the same shape."""
    x = np.array([1.0, 2.0, 3.0])
    y = np.array([1.0, 2.0])

    with pytest.raises(ValueError):
        fit_gaussian_peak(x, y)