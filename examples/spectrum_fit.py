"""
Example: fit a Gaussian peak from a sample spectrum.

This example reads data/spectrum_sample.csv, fits a Gaussian peak using
radlabpy.radiation, calculates the FWHM and resolution, and plots the
result with radlabpy.plotting.

Run from the project root with:

    python examples/spectrum_fit.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from radlabpy.io import read_spectrum_csv
from radlabpy.plotting import plot_gaussian_fit, plot_spectrum
from radlabpy.radiation import (
    energy_resolution,
    fit_gaussian_peak,
    fwhm_from_sigma,
)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "spectrum_sample.csv"

    spectrum = read_spectrum_csv(data_path)

    channels = spectrum["channel"]
    counts = spectrum["counts"]

    fit = fit_gaussian_peak(channels, counts)

    fitted_fwhm = fwhm_from_sigma(fit["sigma"])
    fitted_resolution = energy_resolution(fitted_fwhm, fit["mean"])

    print("Spectrum Gaussian fit")
    print("=====================")
    print(f"Input file: {data_path}")
    print(f"Fitted mean channel: {fit['mean']:.3f}")
    print(f"Fitted amplitude:    {fit['amplitude']:.3f}")
    print(f"Fitted sigma:        {fit['sigma']:.3f}")
    print(f"Fitted FWHM:         {fitted_fwhm:.3f}")
    print(f"Resolution:          {fitted_resolution:.4f}")
    print(f"Background:          {fit['background']:.3f}")

    fig, ax = plot_spectrum(
        channels,
        counts,
        title="Sample spectrum",
        xlabel="Channel",
        ylabel="Counts",
        show_errors=True,
    )

    fig_fit, ax_fit = plot_gaussian_fit(
        channels,
        counts,
        fit,
        title="Gaussian fit to sample spectrum",
        xlabel="Channel",
        ylabel="Counts",
        show_errors=True,
        annotate=True,
    )

    plt.show()


if __name__ == "__main__":
    main()