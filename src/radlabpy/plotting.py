"""
Scientific plotting utilities for radlabpy.

This module provides plotting functions for radiation counting data,
spectra, Gaussian fits, energy calibration and HEP invariant-mass
distributions.

The functions in this module only create figures. They do not save files
automatically and do not call ``plt.show()``.

Design principles
-----------------
- Keep plotting separate from physics calculations.
- Return ``fig, ax`` for all plotting functions.
- Accept an existing Matplotlib axis through ``ax``.
- Use clear labels and publication-friendly defaults.
"""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np

from radlabpy.radiation import gaussian


def _get_fig_ax(ax=None, figsize: tuple[float, float] | None = None):
    """
    Return a Matplotlib figure and axes.

    If ax is None, a new figure and axes are created. Otherwise, the
    existing axes and its parent figure are returned.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    return fig, ax


def _apply_scientific_style(
    ax,
    *,
    grid: bool = True,
    legend: bool = False,
) -> None:
    """
    Apply a simple publication-friendly style to an axis.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axis to style.
    grid : bool, optional
        If True, add a light grid. Default is True.
    legend : bool, optional
        If True, draw a legend. Default is False.
    """
    ax.tick_params(
        direction="in",
        top=True,
        right=True,
        which="both",
    )

    if grid:
        ax.grid(True, alpha=0.3, linestyle="--", linewidth=0.7)

    if legend:
        ax.legend(frameon=True)


def _set_labels_and_title(
    ax,
    *,
    xlabel: str,
    ylabel: str,
    title: str | None,
) -> None:
    """
    Set axis labels and an optional title.
    """
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if title is not None:
        ax.set_title(title)


def _format_parameter_box(parameters: dict[str, Any]) -> str:
    """
    Format a dictionary of parameters as a compact annotation string.
    """
    lines = []

    for key, value in parameters.items():
        if isinstance(value, float):
            lines.append(f"{key} = {value:.4g}")
        else:
            lines.append(f"{key} = {value}")

    return "\n".join(lines)


def _add_annotation_box(
    ax,
    text: str,
    *,
    location: tuple[float, float] = (0.03, 0.97),
) -> None:
    """
    Add a small annotation box in axis coordinates.
    """
    ax.text(
        location[0],
        location[1],
        text,
        transform=ax.transAxes,
        va="top",
        ha="left",
        bbox={
            "boxstyle": "round",
            "facecolor": "white",
            "alpha": 0.85,
            "edgecolor": "0.7",
        },
    )


def plot_counts_time(
    time,
    counts,
    ax=None,
    *,
    xlabel: str = "Time [s]",
    ylabel: str = "Counts",
    title: str | None = None,
    marker: str = "o",
    linestyle: str = "-",
    grid: bool = True,
    figsize: tuple[float, float] | None = (6.5, 4.0),
):
    """
    Plot counts as a function of time.

    Parameters
    ----------
    time : array-like
        Time values.
    counts : array-like
        Count values.
    ax : matplotlib.axes.Axes, optional
        Existing axes to plot on.
    xlabel : str, optional
        Label for the x-axis. Default is ``"Time [s]"``.
    ylabel : str, optional
        Label for the y-axis. Default is ``"Counts"``.
    title : str or None, optional
        Optional plot title. Default is None.
    marker : str, optional
        Marker style. Default is ``"o"``.
    linestyle : str, optional
        Line style. Default is ``"-"``.
    grid : bool, optional
        If True, add a light grid. Default is True.
    figsize : tuple or None, optional
        Figure size used when ``ax=None``.

    Returns
    -------
    tuple
        ``(fig, ax)`` Matplotlib figure and axes.
    """
    fig, ax = _get_fig_ax(ax, figsize=figsize)

    ax.plot(
        time,
        counts,
        marker=marker,
        linestyle=linestyle,
        linewidth=1.5,
        markersize=5,
    )

    _set_labels_and_title(
        ax,
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
    )
    _apply_scientific_style(ax, grid=grid)

    fig.tight_layout()
    return fig, ax


def plot_spectrum(
    channels,
    counts,
    ax=None,
    *,
    xlabel: str = "Channel",
    ylabel: str = "Counts",
    title: str | None = None,
    label: str | None = None,
    errors=None,
    show_errors: bool = False,
    grid: bool = True,
    figsize: tuple[float, float] | None = (6.5, 4.0),
):
    """
    Plot a radiation spectrum.

    Parameters
    ----------
    channels : array-like
        Detector channel values.
    counts : array-like
        Counts per channel.
    ax : matplotlib.axes.Axes, optional
        Existing axes to plot on.
    xlabel : str, optional
        Label for the x-axis. Default is ``"Channel"``.
    ylabel : str, optional
        Label for the y-axis. Default is ``"Counts"``.
    title : str or None, optional
        Optional plot title. Default is None.
    label : str or None, optional
        Optional legend label.
    errors : array-like or None, optional
        Uncertainties in counts. If None and ``show_errors=True``,
        Poisson uncertainties ``sqrt(counts)`` are used.
    show_errors : bool, optional
        If True, draw error bars. Default is False.
    grid : bool, optional
        If True, add a light grid. Default is True.
    figsize : tuple or None, optional
        Figure size used when ``ax=None``.

    Returns
    -------
    tuple
        ``(fig, ax)`` Matplotlib figure and axes.
    """
    fig, ax = _get_fig_ax(ax, figsize=figsize)

    channels_array = np.asarray(channels, dtype=float)
    counts_array = np.asarray(counts, dtype=float)

    if show_errors:
        if errors is None:
            errors = np.sqrt(np.clip(counts_array, 0.0, None))

        ax.errorbar(
            channels_array,
            counts_array,
            yerr=errors,
            fmt="o",
            markersize=4,
            linewidth=1.0,
            capsize=2,
            label=label,
        )
    else:
        ax.step(
            channels_array,
            counts_array,
            where="mid",
            linewidth=1.5,
            label=label,
        )

    _set_labels_and_title(
        ax,
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
    )
    _apply_scientific_style(ax, grid=grid, legend=label is not None)

    fig.tight_layout()
    return fig, ax


def plot_gaussian_fit(
    x,
    y,
    fit_result,
    ax=None,
    *,
    xlabel: str = "Channel",
    ylabel: str = "Counts",
    title: str | None = None,
    data_label: str = "Data",
    fit_label: str = "Gaussian fit",
    show_errors: bool = False,
    errors=None,
    annotate: bool = True,
    grid: bool = True,
    figsize: tuple[float, float] | None = (6.5, 4.0),
):
    """
    Plot data together with a Gaussian fit.

    Parameters
    ----------
    x : array-like
        Independent variable values.
    y : array-like
        Measured counts or intensities.
    fit_result : dict
        Fit result compatible with ``radlabpy.radiation.fit_gaussian_peak``.
        It must contain ``amplitude``, ``mean`` and ``sigma``. The
        ``background`` key is optional and defaults to 0.
    ax : matplotlib.axes.Axes, optional
        Existing axes to plot on.
    xlabel : str, optional
        Label for the x-axis.
    ylabel : str, optional
        Label for the y-axis.
    title : str or None, optional
        Optional plot title.
    data_label : str, optional
        Label for measured data.
    fit_label : str, optional
        Label for Gaussian fit.
    show_errors : bool, optional
        If True, draw Poisson-like error bars for the data.
    errors : array-like or None, optional
        User-provided data uncertainties. If None and ``show_errors=True``,
        uncertainties are estimated as ``sqrt(y)``.
    annotate : bool, optional
        If True, annotate fitted parameters on the plot.
    grid : bool, optional
        If True, add a light grid.
    figsize : tuple or None, optional
        Figure size used when ``ax=None``.

    Returns
    -------
    tuple
        ``(fig, ax)`` Matplotlib figure and axes.

    Raises
    ------
    ValueError
        If required fit-result keys are missing.
    """
    required_keys = ["amplitude", "mean", "sigma"]
    missing_keys = [key for key in required_keys if key not in fit_result]

    if missing_keys:
        raise ValueError(
            "fit_result is missing required key(s): " + ", ".join(missing_keys)
        )

    fig, ax = _get_fig_ax(ax, figsize=figsize)

    x_array = np.asarray(x, dtype=float)
    y_array = np.asarray(y, dtype=float)

    background = fit_result.get("background", 0.0)

    fitted_y = gaussian(
        x_array,
        amplitude=fit_result["amplitude"],
        mean=fit_result["mean"],
        sigma=fit_result["sigma"],
        background=background,
    )

    if show_errors:
        if errors is None:
            errors = np.sqrt(np.clip(y_array, 0.0, None))

        ax.errorbar(
            x_array,
            y_array,
            yerr=errors,
            fmt="o",
            markersize=4,
            linewidth=1.0,
            capsize=2,
            label=data_label,
        )
    else:
        ax.step(
            x_array,
            y_array,
            where="mid",
            linewidth=1.5,
            label=data_label,
        )

    ax.plot(
        x_array,
        fitted_y,
        linewidth=2.0,
        label=fit_label,
    )

    _set_labels_and_title(
        ax,
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
    )

    _apply_scientific_style(ax, grid=grid, legend=True)

    if annotate:
        annotation = _format_parameter_box(
            {
                "A": float(fit_result["amplitude"]),
                "mu": float(fit_result["mean"]),
                "sigma": float(fit_result["sigma"]),
                "bkg": float(background),
            }
        )
        _add_annotation_box(ax, annotation)

    fig.tight_layout()
    return fig, ax


def plot_calibration(
    channels,
    energies,
    calibration,
    ax=None,
    *,
    xlabel: str = "Channel",
    ylabel: str = "Energy",
    title: str | None = None,
    data_label: str = "Calibration points",
    fit_label: str = "Linear calibration",
    annotate: bool = True,
    grid: bool = True,
    figsize: tuple[float, float] | None = (6.5, 4.0),
):
    """
    Plot energy calibration points and the fitted linear calibration.

    The expected calibration convention is:

        E = slope * channel + intercept

    Parameters
    ----------
    channels : array-like
        Calibration channel values.
    energies : array-like
        Known calibration energies.
    calibration : dict
        Dictionary containing at least ``slope`` and ``intercept``.
    ax : matplotlib.axes.Axes, optional
        Existing axes to plot on.
    xlabel : str, optional
        Label for the x-axis.
    ylabel : str, optional
        Label for the y-axis.
    title : str or None, optional
        Optional plot title.
    data_label : str, optional
        Label for calibration points.
    fit_label : str, optional
        Label for the fitted calibration line.
    annotate : bool, optional
        If True, annotate fit parameters.
    grid : bool, optional
        If True, add a light grid.
    figsize : tuple or None, optional
        Figure size used when ``ax=None``.

    Returns
    -------
    tuple
        ``(fig, ax)`` Matplotlib figure and axes.

    Raises
    ------
    ValueError
        If ``slope`` or ``intercept`` are missing from calibration.
    """
    required_keys = ["slope", "intercept"]
    missing_keys = [key for key in required_keys if key not in calibration]

    if missing_keys:
        raise ValueError(
            "calibration is missing required key(s): " + ", ".join(missing_keys)
        )

    fig, ax = _get_fig_ax(ax, figsize=figsize)

    channels_array = np.asarray(channels, dtype=float)
    energies_array = np.asarray(energies, dtype=float)

    channel_grid = np.linspace(np.min(channels_array), np.max(channels_array), 300)
    energy_grid = calibration["slope"] * channel_grid + calibration["intercept"]

    ax.scatter(
        channels_array,
        energies_array,
        s=35,
        label=data_label,
        zorder=3,
    )
    ax.plot(
        channel_grid,
        energy_grid,
        linewidth=1.8,
        label=fit_label,
    )

    _set_labels_and_title(
        ax,
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
    )
    _apply_scientific_style(ax, grid=grid, legend=True)

    if annotate:
        parameters = {
            "slope": float(calibration["slope"]),
            "intercept": float(calibration["intercept"]),
        }

        if "r_squared" in calibration:
            parameters["R^2"] = float(calibration["r_squared"])

        annotation = _format_parameter_box(parameters)
        _add_annotation_box(ax, annotation)

    fig.tight_layout()
    return fig, ax


def plot_calibration_residuals(
    channels,
    residuals,
    ax=None,
    *,
    xlabel: str = "Channel",
    ylabel: str = "Residual",
    title: str | None = None,
    grid: bool = True,
    figsize: tuple[float, float] | None = (6.5, 3.5),
):
    """
    Plot calibration residuals.

    Parameters
    ----------
    channels : array-like
        Calibration channel values.
    residuals : array-like
        Calibration residual values.
    ax : matplotlib.axes.Axes, optional
        Existing axes to plot on.
    xlabel : str, optional
        Label for the x-axis.
    ylabel : str, optional
        Label for the y-axis.
    title : str or None, optional
        Optional plot title.
    grid : bool, optional
        If True, add a light grid.
    figsize : tuple or None, optional
        Figure size used when ``ax=None``.

    Returns
    -------
    tuple
        ``(fig, ax)`` Matplotlib figure and axes.
    """
    fig, ax = _get_fig_ax(ax, figsize=figsize)

    channels_array = np.asarray(channels, dtype=float)
    residuals_array = np.asarray(residuals, dtype=float)

    ax.axhline(
        0.0,
        linestyle="--",
        linewidth=1.2,
        color="0.3",
    )
    ax.scatter(
        channels_array,
        residuals_array,
        s=35,
        zorder=3,
    )

    _set_labels_and_title(
        ax,
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
    )
    _apply_scientific_style(ax, grid=grid)

    if residuals_array.size > 0:
        max_abs = np.max(np.abs(residuals_array))
        if max_abs > 0:
            ax.set_ylim(-1.25 * max_abs, 1.25 * max_abs)

    fig.tight_layout()
    return fig, ax


def plot_invariant_mass(
    masses,
    bins=50,
    ax=None,
    *,
    xlabel: str = "Invariant mass",
    ylabel: str = "Events",
    title: str | None = None,
    label: str | None = None,
    histtype: str = "stepfilled",
    alpha: float = 0.75,
    grid: bool = True,
    figsize: tuple[float, float] | None = (6.5, 4.0),
):
    """
    Plot an invariant-mass distribution.

    Parameters
    ----------
    masses : array-like
        Invariant-mass values.
    bins : int or sequence, optional
        Number of histogram bins or bin edges. Default is 50.
    ax : matplotlib.axes.Axes, optional
        Existing axes to plot on.
    xlabel : str, optional
        Label for the x-axis.
    ylabel : str, optional
        Label for the y-axis.
    title : str or None, optional
        Optional plot title.
    label : str or None, optional
        Optional legend label.
    histtype : str, optional
        Matplotlib histogram type. Default is ``"stepfilled"``.
    alpha : float, optional
        Histogram transparency. Default is 0.75.
    grid : bool, optional
        If True, add a light grid.
    figsize : tuple or None, optional
        Figure size used when ``ax=None``.

    Returns
    -------
    tuple
        ``(fig, ax)`` Matplotlib figure and axes.
    """
    fig, ax = _get_fig_ax(ax, figsize=figsize)

    masses_array = np.asarray(masses, dtype=float)

    ax.hist(
        masses_array,
        bins=bins,
        histtype=histtype,
        alpha=alpha,
        edgecolor="black",
        linewidth=1.0,
        label=label,
    )

    _set_labels_and_title(
        ax,
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
    )
    _apply_scientific_style(ax, grid=grid, legend=label is not None)

    fig.tight_layout()
    return fig, ax