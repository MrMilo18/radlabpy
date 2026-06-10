"""Unit tests for basic spectrum utilities."""

import math

import numpy as np
import pytest

from radlabpy.radiation import (
    find_peak_channel,
    normalize_spectrum,
    total_counts,
)


def test_total_counts():
    """total_counts should return the sum of all counts."""
    counts = [10, 20, 30]

    result = total_counts(counts)

    assert math.isclose(result, 60.0, rel_tol=1e-12)


def test_total_counts_empty_input():
    """Empty counts should raise ValueError."""
    with pytest.raises(ValueError):
        total_counts([])


def test_total_counts_negative_values():
    """Negative counts should raise ValueError."""
    with pytest.raises(ValueError):
        total_counts([10, -1, 20])


def test_normalize_spectrum():
    """normalize_spectrum should return an array whose sum is 1."""
    counts = [10, 20, 30]

    normalized = normalize_spectrum(counts)

    assert np.allclose(normalized, np.array([1 / 6, 2 / 6, 3 / 6]))
    assert math.isclose(np.sum(normalized), 1.0, rel_tol=1e-12)


def test_normalize_spectrum_zero_total():
    """A spectrum with zero total counts cannot be normalized."""
    with pytest.raises(ValueError):
        normalize_spectrum([0, 0, 0])


def test_find_peak_channel():
    """find_peak_channel should return the channel with maximum counts."""
    channels = [0, 1, 2, 3, 4]
    counts = [5, 10, 50, 20, 3]

    peak_channel = find_peak_channel(channels, counts)

    assert math.isclose(peak_channel, 2.0, rel_tol=1e-12)


def test_find_peak_channel_invalid_shapes():
    """channels and counts must have the same shape."""
    channels = [0, 1, 2]
    counts = [10, 20]

    with pytest.raises(ValueError):
        find_peak_channel(channels, counts)


def test_find_peak_channel_empty_input():
    """Empty channels/counts should raise ValueError."""
    with pytest.raises(ValueError):
        find_peak_channel([], [])