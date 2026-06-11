"""
Tests for radlabpy.plotting.
"""

from __future__ import annotations

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pytest

from radlabpy.plotting import (
    plot_calibration,
    plot_calibration_residuals,
    plot_counts_time,
    plot_gaussian_fit,
    plot_invariant_mass,
    plot_spectrum,
)
from radlabpy.radiation import fit_gaussian_peak, gaussian, linear_calibration


def _assert_fig_ax(fig, ax):
    assert isinstance(fig, matplotlib.figure.Figure)
    assert isinstance(ax, matplotlib.axes.Axes)


def test_plot_counts_time_returns_fig_ax():
    time = np.array([0.0, 1.0, 2.0])
    counts = np.array([20, 25, 23])

    fig, ax = plot_counts_time(time, counts)

    _assert_fig_ax(fig, ax)
    plt.close(fig)


def test_plot_spectrum_returns_fig_ax_with_simple_data():
    channels = np.array([0, 1, 2, 3])
    counts = np.array([5, 10, 7, 3])

    fig, ax = plot_spectrum(channels, counts)

    _assert_fig_ax(fig, ax)
    plt.close(fig)


def test_plot_gaussian_fit_returns_fig_ax_with_fit_result():
    x = np.linspace(0.0, 100.0, 201)

    y = gaussian(
        x,
        amplitude=100.0,
        mean=50.0,
        sigma=5.0,
        background=10.0,
    )

    fit_result = fit_gaussian_peak(x, y)

    fig, ax = plot_gaussian_fit(x, y, fit_result)

    _assert_fig_ax(fig, ax)
    plt.close(fig)


def test_plot_calibration_returns_fig_ax():
    channels = np.array([0.0, 100.0, 200.0, 300.0])
    energies = np.array([0.0, 50.0, 100.0, 150.0])

    calibration = linear_calibration(channels, energies)

    fig, ax = plot_calibration(channels, energies, calibration)

    _assert_fig_ax(fig, ax)
    plt.close(fig)


def test_plot_calibration_residuals_returns_fig_ax():
    channels = np.array([0.0, 100.0, 200.0, 300.0])
    residuals = np.array([0.0, 0.2, -0.1, 0.1])

    fig, ax = plot_calibration_residuals(channels, residuals)

    _assert_fig_ax(fig, ax)
    plt.close(fig)


def test_plot_invariant_mass_returns_fig_ax_with_array():
    masses = np.array([88.0, 89.5, 90.1, 91.2, 92.0, 93.5])

    fig, ax = plot_invariant_mass(masses, bins=5)

    _assert_fig_ax(fig, ax)
    plt.close(fig)


def test_plot_invariant_mass_accepts_list():
    masses = [88.0, 89.5, 90.1, 91.2, 92.0, 93.5]

    fig, ax = plot_invariant_mass(masses, bins=5)

    _assert_fig_ax(fig, ax)
    plt.close(fig)


def test_plot_functions_accept_existing_axes():
    channels = np.array([0, 1, 2])
    counts = np.array([10, 20, 15])

    fig, ax = plt.subplots()
    returned_fig, returned_ax = plot_spectrum(channels, counts, ax=ax)

    assert returned_fig is fig
    assert returned_ax is ax

    plt.close(fig)


def test_plot_functions_do_not_call_show(monkeypatch):
    def fake_show():
        raise AssertionError("plt.show() should not be called inside plotting functions.")

    monkeypatch.setattr(plt, "show", fake_show)

    channels = np.array([0, 1, 2])
    counts = np.array([10, 20, 15])

    fig, ax = plot_spectrum(channels, counts)

    _assert_fig_ax(fig, ax)
    plt.close(fig)


def test_plot_gaussian_fit_missing_key_raises_value_error():
    x = np.linspace(0.0, 10.0, 11)
    y = np.ones_like(x)

    bad_fit_result = {
        "amplitude": 1.0,
        "mean": 5.0,
    }

    with pytest.raises(ValueError, match="missing required key"):
        plot_gaussian_fit(x, y, bad_fit_result)


def test_plot_calibration_missing_key_raises_value_error():
    channels = np.array([0.0, 1.0, 2.0])
    energies = np.array([0.0, 1.0, 2.0])

    bad_calibration = {
        "slope": 1.0,
    }

    with pytest.raises(ValueError, match="missing required key"):
        plot_calibration(channels, energies, bad_calibration)