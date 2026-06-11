"""
Invariant mass demo using radlabpy.hep.

This example reads a small HEP-like event table from
data/hep_events_sample.csv and computes invariant masses for simple
two-event systems.

The example uses natural units with c = 1.

Run from the project root with:

    python examples/invariant_mass_demo.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from radlabpy.hep import delta_r, eta, invariant_mass, phi, pt
from radlabpy.io import read_event_table
from radlabpy.plotting import plot_invariant_mass


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "hep_events_sample.csv"

    events = read_event_table(data_path)

    print("HEP invariant-mass demo")
    print("=======================")
    print(f"Input file: {data_path}")
    print(f"Number of rows: {len(events)}")

    masses = []

    print()
    print("Single-object observables")
    print("=========================")

    for _, row in events.iterrows():
        object_pt = pt(row["px"], row["py"])
        object_eta = eta(row["px"], row["py"], row["pz"])
        object_phi = phi(row["px"], row["py"])

        print(
            f"Event {int(row['event'])}: "
            f"pt = {object_pt:8.3f}, "
            f"eta = {object_eta:8.3f}, "
            f"phi = {object_phi:8.3f}"
        )

    print()
    print("Two-object invariant masses")
    print("===========================")

    for i in range(0, len(events) - 1, 2):
        row_1 = events.iloc[i]
        row_2 = events.iloc[i + 1]

        total_E = row_1["E"] + row_2["E"]
        total_px = row_1["px"] + row_2["px"]
        total_py = row_1["py"] + row_2["py"]
        total_pz = row_1["pz"] + row_2["pz"]

        mass = invariant_mass(total_E, total_px, total_py, total_pz)
        masses.append(mass)

        eta_1 = eta(row_1["px"], row_1["py"], row_1["pz"])
        eta_2 = eta(row_2["px"], row_2["py"], row_2["pz"])
        phi_1 = phi(row_1["px"], row_1["py"])
        phi_2 = phi(row_2["px"], row_2["py"])

        dr = delta_r(eta_1, phi_1, eta_2, phi_2)

        print(
            f"Events {int(row_1['event'])}-{int(row_2['event'])}: "
            f"mass = {mass:8.3f}, "
            f"Delta R = {dr:8.3f}"
        )

    masses = np.asarray(masses, dtype=float)

    print()
    print("Mass distribution summary")
    print("=========================")
    print(f"Number of masses: {masses.size}")
    print(f"Mean mass:        {np.mean(masses):.6f}")
    print(f"Std mass:         {np.std(masses, ddof=1):.6f}")

    fig, ax = plot_invariant_mass(
        masses,
        bins=5,
        title="Sample invariant-mass distribution",
        xlabel="Invariant mass [GeV]",
        ylabel="Events",
    )

    plt.show()


if __name__ == "__main__":
    main()