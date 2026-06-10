"""Example: fit a synthetic Gaussian peak spectrum.

This example generates a simple synthetic radiation spectrum with a
Gaussian peak plus constant background. Then it fits the peak using
radlabpy, calculates the FWHM and relative resolution, and optionally
plots the result.
"""

import numpy as np

from radlabpy.radiation import (
    energy_resolution,
    fit_gaussian_peak,
    fwhm_from_sigma,
    gaussian,
)


def main():
    """Run the synthetic spectrum fitting example."""
    rng = np.random.default_rng(seed=42)

    channels = np.linspace(0.0, 200.0, 401)

    true_amplitude = 500.0
    true_mean = 100.0
    true_sigma = 8.0
    true_background = 25.0

    expected_counts = gaussian(
        channels,
        amplitude=true_amplitude,
        mean=true_mean,
        sigma=true_sigma,
        background=true_background,
    )

    counts = rng.poisson(expected_counts)

    fit = fit_gaussian_peak(channels, counts)

    fitted_fwhm = fwhm_from_sigma(fit["sigma"])
    fitted_resolution = energy_resolution(fitted_fwhm, fit["mean"])

    print("Synthetic spectrum Gaussian fit")
    print("--------------------------------")
    print(f"True mean:        {true_mean:.3f}")
    print(f"Fitted mean:      {fit['mean']:.3f}")
    print(f"Fitted amplitude: {fit['amplitude']:.3f}")
    print(f"Fitted sigma:     {fit['sigma']:.3f}")
    print(f"Fitted FWHM:      {fitted_fwhm:.3f}")
    print(f"Resolution:       {fitted_resolution:.4f}")
    print(f"Background:       {fit['background']:.3f}")

    try:
        import matplotlib.pyplot as plt

        fitted_counts = gaussian(
            channels,
            amplitude=fit["amplitude"],
            mean=fit["mean"],
            sigma=fit["sigma"],
            background=fit["background"],
        )

        fig, ax = plt.subplots()
        ax.step(channels, counts, where="mid", label="Synthetic spectrum")
        ax.plot(channels, fitted_counts, label="Gaussian fit")
        ax.set_xlabel("Channel")
        ax.set_ylabel("Counts")
        ax.set_title("Synthetic Gaussian peak fit")
        ax.legend()

        plt.show()

    except ImportError:
        print("matplotlib is not installed; skipping plot.")


if __name__ == "__main__":
    main()