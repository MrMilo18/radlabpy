"""
Example: linear energy calibration for a radiation spectrum.

This example shows how to:

1. Create synthetic channel-energy calibration data.
2. Fit a linear calibration.
3. Convert new detector channels to energies.
4. Convert energies back to channels.
5. Compute calibration residuals.
6. Plot the calibration curve and residuals.
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from radlabpy.radiation import (
    linear_calibration,
    channel_to_energy,
    energy_to_channel,
    calibration_residuals,
)


def main() -> None:
    # Synthetic calibration data.
    # Convention: E = slope * channel + intercept
    channels = np.array([0, 100, 200, 300, 400], dtype=float)
    energies = np.array([0, 50, 100, 150, 200], dtype=float)

    calibration = linear_calibration(channels, energies)

    print("Linear energy calibration")
    print("-------------------------")
    print(f"Slope:      {calibration['slope']:.6f}")
    print(f"Intercept:  {calibration['intercept']:.6f}")
    print(f"r value:    {calibration['r_value']:.6f}")
    print(f"r squared:  {calibration['r_squared']:.6f}")

    new_channels = np.array([50, 150, 250, 350], dtype=float)
    calibrated_energies = channel_to_energy(new_channels, calibration)

    print("\nChannel to energy conversion")
    print("----------------------------")
    for channel, energy in zip(new_channels, calibrated_energies):
        print(f"Channel {channel:7.2f} -> Energy {energy:7.2f}")

    test_energies = np.array([25, 75, 125, 175], dtype=float)
    reconstructed_channels = energy_to_channel(test_energies, calibration)

    print("\nEnergy to channel conversion")
    print("----------------------------")
    for energy, channel in zip(test_energies, reconstructed_channels):
        print(f"Energy {energy:7.2f} -> Channel {channel:7.2f}")

    residuals = calibration_residuals(channels, energies, calibration)

    print("\nCalibration residuals")
    print("---------------------")
    for channel, residual in zip(channels, residuals):
        print(f"Channel {channel:7.2f} -> Residual {residual: .3e}")

    # Plot calibration curve.
    channel_grid = np.linspace(np.min(channels), np.max(channels), 200)
    energy_grid = channel_to_energy(channel_grid, calibration)

    fig, ax = plt.subplots()
    ax.scatter(channels, energies, label="Calibration points")
    ax.plot(channel_grid, energy_grid, label="Linear fit")
    ax.set_xlabel("Channel")
    ax.set_ylabel("Energy")
    ax.set_title("Linear energy calibration")
    ax.legend()
    fig.tight_layout()

    # Plot residuals.
    fig_res, ax_res = plt.subplots()
    ax_res.axhline(0.0, linestyle="--")
    ax_res.scatter(channels, residuals)
    ax_res.set_xlabel("Channel")
    ax_res.set_ylabel("Residual")
    ax_res.set_title("Calibration residuals")
    fig_res.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()