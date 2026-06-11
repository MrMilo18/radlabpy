"""
Example: linear energy calibration for a radiation spectrum.

This example shows how to:

1. Create simple channel-energy calibration data.
2. Fit a linear calibration.
3. Convert channels to energies.
4. Convert energies back to channels.
5. Compute calibration residuals.
6. Plot the calibration and residuals with radlabpy.plotting.

Run from the project root with:

    python examples/energy_calibration.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from radlabpy.plotting import plot_calibration, plot_calibration_residuals
from radlabpy.radiation import (
    calibration_residuals,
    channel_to_energy,
    energy_to_channel,
    linear_calibration,
)


def main() -> None:
    # Synthetic calibration data.
    # Convention: E = slope * channel + intercept
    channels = np.array([0, 100, 200, 300, 400], dtype=float)
    energies = np.array([0, 50, 100, 150, 200], dtype=float)

    calibration = linear_calibration(channels, energies)

    print("Linear energy calibration")
    print("=========================")
    print(f"Slope:     {calibration['slope']:.6f}")
    print(f"Intercept: {calibration['intercept']:.6f}")
    print(f"r value:   {calibration['r_value']:.6f}")
    print(f"r squared: {calibration['r_squared']:.6f}")

    new_channels = np.array([50, 150, 250, 350], dtype=float)
    calibrated_energies = channel_to_energy(new_channels, calibration)

    print()
    print("Channel to energy conversion")
    print("============================")
    for channel, energy_value in zip(new_channels, calibrated_energies):
        print(f"Channel {channel:7.2f} -> Energy {energy_value:7.2f}")

    test_energies = np.array([25, 75, 125, 175], dtype=float)
    reconstructed_channels = energy_to_channel(test_energies, calibration)

    print()
    print("Energy to channel conversion")
    print("============================")
    for energy_value, channel in zip(test_energies, reconstructed_channels):
        print(f"Energy {energy_value:7.2f} -> Channel {channel:7.2f}")

    residuals = calibration_residuals(channels, energies, calibration)

    print()
    print("Calibration residuals")
    print("=====================")
    for channel, residual in zip(channels, residuals):
        print(f"Channel {channel:7.2f} -> Residual {residual: .3e}")

    fig, ax = plot_calibration(
        channels,
        energies,
        calibration,
        title="Linear energy calibration",
        xlabel="Channel",
        ylabel="Energy [a.u.]",
        annotate=True,
    )

    fig_res, ax_res = plot_calibration_residuals(
        channels,
        residuals,
        title="Calibration residuals",
        xlabel="Channel",
        ylabel="Residual [a.u.]",
    )

    plt.show()


if __name__ == "__main__":
    main()