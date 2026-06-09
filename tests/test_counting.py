import math

import numpy as np
import pytest

from radlabpy.radiation import (
    poisson_uncertainty,
    counting_summary,
    count_rate,
    cps_to_cpm,
    cpm_to_cps,
)


def test_poisson_uncertainty_scalar():
    result = poisson_uncertainty(100)
    assert math.isclose(result, 10.0, rel_tol=1e-12)

 
def test_poisson_uncertainty_array():
    counts = np.array([0, 1, 4, 9, 100])
    result = poisson_uncertainty(counts)
    expected = np.array([0, 1, 2, 3, 10])
    np.testing.assert_allclose(result, expected)


def test_poisson_uncertainty_negative_counts():
    with pytest.raises(ValueError):
        poisson_uncertainty(-1)


def test_counting_summary_basic_values():
    counts = [20, 25, 30]
    summary = counting_summary(counts)

    assert summary["n_measurements"] == 3
    assert math.isclose(summary["total_counts"], 75.0, rel_tol=1e-12)
    assert math.isclose(summary["mean_counts"], 25.0, rel_tol=1e-12)
    assert math.isclose(summary["min_counts"], 20.0, rel_tol=1e-12)
    assert math.isclose(summary["max_counts"], 30.0, rel_tol=1e-12)
    assert math.isclose(summary["poisson_uncertainty_mean"], 5.0, rel_tol=1e-12)


def test_counting_summary_empty_counts():
    with pytest.raises(ValueError):
        counting_summary([])


def test_counting_summary_negative_counts():
    with pytest.raises(ValueError):
        counting_summary([10, -2, 5])


def test_count_rate_scalar():
    result = count_rate(120, 60)
    assert math.isclose(result, 2.0, rel_tol=1e-12)


def test_count_rate_array():
    counts = np.array([60, 120, 180])
    time = 60
    result = count_rate(counts, time)
    expected = np.array([1, 2, 3])
    np.testing.assert_allclose(result, expected)


def test_count_rate_zero_time():
    with pytest.raises(ValueError):
        count_rate(100, 0)


def test_count_rate_negative_time():
    with pytest.raises(ValueError):
        count_rate(100, -5)


def test_count_rate_negative_counts():
    with pytest.raises(ValueError):
        count_rate(-10, 5)


def test_cps_to_cpm_scalar():
    result = cps_to_cpm(2)
    assert math.isclose(result, 120.0, rel_tol=1e-12)


def test_cpm_to_cps_scalar():
    result = cpm_to_cps(120)
    assert math.isclose(result, 2.0, rel_tol=1e-12)


def test_cps_to_cpm_and_back():
    cps = np.array([0.5, 1.0, 2.0, 3.0])
    cpm = cps_to_cpm(cps)
    recovered_cps = cpm_to_cps(cpm)

    np.testing.assert_allclose(recovered_cps, cps)


def test_cps_to_cpm_negative_value():
    with pytest.raises(ValueError):
        cps_to_cpm(-1)


def test_cpm_to_cps_negative_value():
    with pytest.raises(ValueError):
        cpm_to_cps(-60)