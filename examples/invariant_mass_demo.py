"""
Invariant mass demo using radlabpy.hep.

This example shows how to calculate basic high-energy physics observables
from simple four-momenta using natural units with c = 1.
"""

from __future__ import annotations

import numpy as np

from radlabpy.hep import (
    delta_r,
    energy,
    eta,
    invariant_mass,
    phi,
    pt,
)


def main():
    # ------------------------------------------------------------------
    # Example 1: two simple particles
    # ------------------------------------------------------------------
    # Units are assumed to be compatible, for example GeV.
    # We use natural units with c = 1.

    particle_1 = {
        "px": 30.0,
        "py": 10.0,
        "pz": 40.0,
        "mass": 0.105,  # approximately a muon mass in GeV
    }

    particle_2 = {
        "px": -20.0,
        "py": -5.0,
        "pz": -30.0,
        "mass": 0.105,
    }

    # Calculate individual energies.
    E1 = energy(
        particle_1["px"],
        particle_1["py"],
        particle_1["pz"],
        particle_1["mass"],
    )

    E2 = energy(
        particle_2["px"],
        particle_2["py"],
        particle_2["pz"],
        particle_2["mass"],
    )

    # Sum the four-momentum components.
    E_total = E1 + E2
    px_total = particle_1["px"] + particle_2["px"]
    py_total = particle_1["py"] + particle_2["py"]
    pz_total = particle_1["pz"] + particle_2["pz"]

    # Calculate invariant mass of the two-particle system.
    m_system = invariant_mass(E_total, px_total, py_total, pz_total)

    # Calculate observables for each particle.
    pt1 = pt(particle_1["px"], particle_1["py"])
    pt2 = pt(particle_2["px"], particle_2["py"])

    eta1 = eta(particle_1["px"], particle_1["py"], particle_1["pz"])
    eta2 = eta(particle_2["px"], particle_2["py"], particle_2["pz"])

    phi1 = phi(particle_1["px"], particle_1["py"])
    phi2 = phi(particle_2["px"], particle_2["py"])

    dr12 = delta_r(eta1, phi1, eta2, phi2)

    print("=== Two-particle invariant mass demo ===")
    print()
    print("Particle 1:")
    print(f"  E   = {E1:.6f}")
    print(f"  pt  = {pt1:.6f}")
    print(f"  eta = {eta1:.6f}")
    print(f"  phi = {phi1:.6f} rad")
    print()
    print("Particle 2:")
    print(f"  E   = {E2:.6f}")
    print(f"  pt  = {pt2:.6f}")
    print(f"  eta = {eta2:.6f}")
    print(f"  phi = {phi2:.6f} rad")
    print()
    print("Two-particle system:")
    print(f"  E_total  = {E_total:.6f}")
    print(f"  px_total = {px_total:.6f}")
    print(f"  py_total = {py_total:.6f}")
    print(f"  pz_total = {pz_total:.6f}")
    print(f"  invariant mass = {m_system:.6f}")
    print()
    print(f"Delta R between particles = {dr12:.6f}")

    # ------------------------------------------------------------------
    # Example 2: small synthetic invariant-mass distribution
    # ------------------------------------------------------------------
    rng = np.random.default_rng(seed=42)

    n_events = 1000

    # Create a simple synthetic distribution around the system mass.
    synthetic_masses = rng.normal(loc=m_system, scale=2.0, size=n_events)

    # Keep only positive masses.
    synthetic_masses = synthetic_masses[synthetic_masses > 0]

    print()
    print("=== Synthetic invariant-mass distribution ===")
    print(f"Number of generated masses = {synthetic_masses.size}")
    print(f"Mean mass                  = {np.mean(synthetic_masses):.6f}")
    print(f"Standard deviation         = {np.std(synthetic_masses, ddof=1):.6f}")
    print(f"Minimum mass               = {np.min(synthetic_masses):.6f}")
    print(f"Maximum mass               = {np.max(synthetic_masses):.6f}")


if __name__ == "__main__":
    main()