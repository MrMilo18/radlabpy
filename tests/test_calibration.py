import math

import numpy as np
import pytest

from radlabpy.radiation import (
    linear_calibration,
    channel_to_energy,
    energy_to_channel,
    calibration_residuals,
)


def test_linear_calibration_recovers_slope_and_intercept():
    channels = [0, 100, 200]
    energies = [0, 50, 100]

    calibration = linear_calibration(channels, energies)

    assert math.isclose(calibration["slope"], 0.5, rel_tol=1e-12)
    assert math.isclose(calibration["intercept"], 0.0, abs_tol=1e-12)
    assert math.isclose(calibration["r_value"], 1.0, rel_tol=1e-12)
    assert math.isclose(calibration["r_squared"], 1.0, rel_tol=1e-12)


def test_channel_to_energy_scalar():
    channels = [0, 100, 200]
    energies = [0, 50, 100]
    calibration = linear_calibration(channels, energies)

    result = channel_to_energy(200, calibration)

    assert math.isclose(result, 100.0, rel_tol=1e-12)


def test_energy_to_channel_scalar():
    channels = [0, 100, 200]
    energies = [0, 50, 100]
    calibration = linear_calibration(channels, energies)

    result = energy_to_channel(100, calibration)

    assert math.isclose(result, 200.0, rel_tol=1e-12)


def test_channel_to_energy_array():
    channels = [0, 100, 200]
    energies = [0, 50, 100]
    calibration = linear_calibration(channels, energies)

    new_channels = [50, 150, 250]
    result = channel_to_energy(new_channels, calibration)

    expected = np.array([25.0, 75.0, 125.0])
    assert np.allclose(result, expected, rtol=1e-12)


def test_energy_to_channel_array():
    channels = [0, 100, 200]
    energies = [0, 50, 100]
    calibration = linear_calibration(channels, energies)

    new_energies = [25, 75, 125]
    result = energy_to_channel(new_energies, calibration)

    expected = np.array([50.0, 150.0, 250.0])
    assert np.allclose(result, expected, rtol=1e-12)


def test_calibration_residuals_are_zero_for_perfect_line():
    channels = [0, 100, 200]
    energies = [0, 50, 100]
    calibration = linear_calibration(channels, energies)

    residuals = calibration_residuals(channels, energies, calibration)

    assert np.allclose(residuals, np.zeros(3), atol=1e-12)


def test_different_lengths_raise_value_error():
    channels = [0, 100, 200]
    energies = [0, 50]

    with pytest.raises(ValueError):
        linear_calibration(channels, energies)


def test_less_than_two_points_raise_value_error():
    channels = [100]
    energies = [50]

    with pytest.raises(ValueError):
        linear_calibration(channels, energies)


def test_empty_channels_raise_value_error():
    channels = []
    energies = []

    with pytest.raises(ValueError):
        linear_calibration(channels, energies)


def test_non_numeric_channels_raise_value_error():
    channels = [0, "bad", 200]
    energies = [0, 50, 100]

    with pytest.raises(ValueError):
        linear_calibration(channels, energies)


def test_zero_slope_raises_value_error():
    channels = [0, 100, 200]
    energies = [50, 50, 50]

    with pytest.raises(ValueError):
        linear_calibration(channels, energies)


def test_invalid_calibration_raises_value_error():
    bad_calibration = {
        "slope": 0.0,
        "intercept": 0.0,
    }

    with pytest.raises(ValueError):
        channel_to_energy(100, bad_calibration)