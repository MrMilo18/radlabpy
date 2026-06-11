import math

import numpy as np
import pytest

from radlabpy.detectors import (
    accidental_coincidence_rate,
    coincidence_rate,
    detection_efficiency,
    efficiency_uncertainty,
    event_rate,
    rate_uncertainty,
    signal_to_noise,
)


def test_detection_efficiency_scalar():
    result = detection_efficiency(50, 100)

    assert math.isclose(result, 0.5, rel_tol=1e-12)


def test_efficiency_uncertainty_positive():
    result = efficiency_uncertainty(50, 100)

    assert result > 0


def test_efficiency_uncertainty_known_value():
    result = efficiency_uncertainty(50, 100)

    assert math.isclose(result, 0.05, rel_tol=1e-12)


def test_detection_efficiency_detected_greater_than_emitted_raises():
    with pytest.raises(ValueError):
        detection_efficiency(120, 100)


def test_detection_efficiency_emitted_zero_raises():
    with pytest.raises(ValueError):
        detection_efficiency(50, 0)


def test_detection_efficiency_emitted_negative_raises():
    with pytest.raises(ValueError):
        detection_efficiency(50, -100)


def test_detection_efficiency_negative_detected_raises():
    with pytest.raises(ValueError):
        detection_efficiency(-1, 100)


def test_event_rate_scalar():
    result = event_rate(100, 20)

    assert math.isclose(result, 5.0, rel_tol=1e-12)


def test_rate_uncertainty_scalar():
    result = rate_uncertainty(100, 20)

    assert math.isclose(result, 0.5, rel_tol=1e-12)


def test_event_rate_time_zero_raises():
    with pytest.raises(ValueError):
        event_rate(100, 0)


def test_event_rate_time_negative_raises():
    with pytest.raises(ValueError):
        event_rate(100, -20)


def test_event_rate_negative_counts_raises():
    with pytest.raises(ValueError):
        event_rate(-100, 20)


def test_coincidence_rate_scalar():
    result = coincidence_rate(30, 10)

    assert math.isclose(result, 3.0, rel_tol=1e-12)


def test_coincidence_rate_negative_coincidences_raises():
    with pytest.raises(ValueError):
        coincidence_rate(-1, 10)


def test_coincidence_rate_time_zero_raises():
    with pytest.raises(ValueError):
        coincidence_rate(30, 0)


def test_accidental_coincidence_rate_scalar():
    result = accidental_coincidence_rate(10, 20, 1e-6)

    assert math.isclose(result, 0.0004, rel_tol=1e-12)


def test_accidental_coincidence_rate_negative_rate_raises():
    with pytest.raises(ValueError):
        accidental_coincidence_rate(-10, 20, 1e-6)


def test_accidental_coincidence_rate_zero_window_raises():
    with pytest.raises(ValueError):
        accidental_coincidence_rate(10, 20, 0)


def test_signal_to_noise_scalar():
    result = signal_to_noise(10, 2)

    assert math.isclose(result, 5.0, rel_tol=1e-12)


def test_signal_to_noise_zero_noise_raises():
    with pytest.raises(ValueError):
        signal_to_noise(10, 0)


def test_signal_to_noise_negative_noise_raises():
    with pytest.raises(ValueError):
        signal_to_noise(10, -2)


def test_detection_efficiency_numpy_arrays():
    detected = np.array([50, 80, 90])
    emitted = np.array([100, 100, 100])

    result = detection_efficiency(detected, emitted)

    expected = np.array([0.5, 0.8, 0.9])
    assert np.allclose(result, expected)


def test_efficiency_uncertainty_numpy_arrays():
    detected = np.array([50, 80, 90])
    emitted = np.array([100, 100, 100])

    result = efficiency_uncertainty(detected, emitted)

    assert isinstance(result, np.ndarray)
    assert result.shape == detected.shape
    assert np.all(result >= 0)


def test_event_rate_numpy_arrays():
    counts = np.array([100, 200, 300])
    time = np.array([10, 20, 30])

    result = event_rate(counts, time)

    expected = np.array([10.0, 10.0, 10.0])
    assert np.allclose(result, expected)


def test_rate_uncertainty_numpy_arrays():
    counts = np.array([100, 400, 900])
    time = np.array([10, 20, 30])

    result = rate_uncertainty(counts, time)

    expected = np.array([1.0, 1.0, 1.0])
    assert np.allclose(result, expected)


def test_coincidence_rate_numpy_arrays():
    coincidences = np.array([30, 60, 90])
    time = np.array([10, 20, 30])

    result = coincidence_rate(coincidences, time)

    expected = np.array([3.0, 3.0, 3.0])
    assert np.allclose(result, expected)


def test_accidental_coincidence_rate_numpy_arrays():
    rate1 = np.array([10, 20, 30])
    rate2 = np.array([20, 30, 40])
    window = 1e-6

    result = accidental_coincidence_rate(rate1, rate2, window)

    expected = 2.0 * rate1 * rate2 * window
    assert np.allclose(result, expected)


def test_signal_to_noise_numpy_arrays():
    signal = np.array([10, 20, 30])
    noise = np.array([2, 4, 5])

    result = signal_to_noise(signal, noise)

    expected = np.array([5.0, 5.0, 6.0])
    assert np.allclose(result, expected)


def test_non_finite_inputs_raise_value_error():
    with pytest.raises(ValueError):
        event_rate(np.array([100, np.nan]), 10)

    with pytest.raises(ValueError):
        detection_efficiency(50, np.inf)

    with pytest.raises(ValueError):
        accidental_coincidence_rate(10, np.nan, 1e-6)

    with pytest.raises(ValueError):
        signal_to_noise(10, np.inf)