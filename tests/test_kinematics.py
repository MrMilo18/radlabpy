import math

import numpy as np
import pytest

from radlabpy.hep import (
    delta_phi,
    delta_r,
    energy,
    eta,
    invariant_mass,
    momentum,
    phi,
    pt,
)


def test_pt_scalar():
    assert math.isclose(pt(3, 4), 5.0, rel_tol=1e-12)


def test_momentum_scalar():
    assert math.isclose(momentum(1, 2, 2), 3.0, rel_tol=1e-12)


def test_energy_particle_at_rest():
    assert math.isclose(energy(0, 0, 0, 1), 1.0, rel_tol=1e-12)


def test_phi_x_axis():
    assert math.isclose(phi(1, 0), 0.0, abs_tol=1e-12)


def test_phi_y_axis():
    assert math.isclose(phi(0, 1), np.pi / 2.0, rel_tol=1e-12)


def test_eta_transverse_particle():
    assert math.isclose(eta(1, 0, 0), 0.0, abs_tol=1e-12)


def test_invariant_mass_particle_at_rest():
    assert math.isclose(invariant_mass(10, 0, 0, 0), 10.0, rel_tol=1e-12)


def test_invariant_mass_known_four_momentum():
    # m^2 = E^2 - px^2 - py^2 - pz^2 = 5^2 - 3^2 - 4^2 = 0
    assert math.isclose(invariant_mass(5, 3, 4, 0), 0.0, abs_tol=1e-12)


def test_invariant_mass_small_negative_roundoff_is_clipped_to_zero():
    # Slightly negative m^2 within tolerance should be treated as zero.
    result = invariant_mass(1.0, 1.0 + 1e-13, 0.0, 0.0, tolerance=1e-12)
    assert math.isclose(result, 0.0, abs_tol=1e-12)


def test_invariant_mass_large_negative_raises_error():
    with pytest.raises(ValueError):
        invariant_mass(1.0, 2.0, 0.0, 0.0)


def test_delta_phi_near_pi_boundary():
    phi1 = np.pi - 0.1
    phi2 = -np.pi + 0.1

    result = delta_phi(phi1, phi2)

    assert math.isclose(abs(result), 0.2, rel_tol=1e-12)


def test_delta_r_same_object_is_zero():
    assert math.isclose(delta_r(1.2, 0.5, 1.2, 0.5), 0.0, abs_tol=1e-12)


def test_numpy_array_inputs():
    px = np.array([3.0, 0.0])
    py = np.array([4.0, 1.0])
    pz = np.array([0.0, 2.0])
    mass = np.array([1.0, 1.0])

    np.testing.assert_allclose(pt(px, py), np.array([5.0, 1.0]))
    np.testing.assert_allclose(momentum(px, py, pz), np.array([5.0, np.sqrt(5.0)]))
    np.testing.assert_allclose(
        energy(px, py, pz, mass),
        np.sqrt(px**2 + py**2 + pz**2 + mass**2),
    )


def test_eta_zero_momentum_raises_error():
    with pytest.raises(ValueError):
        eta(0.0, 0.0, 0.0)


def test_energy_negative_mass_raises_error():
    with pytest.raises(ValueError):
        energy(0.0, 0.0, 0.0, -1.0)


def test_non_finite_input_raises_error():
    with pytest.raises(ValueError):
        pt(np.nan, 1.0)

    with pytest.raises(ValueError):
        invariant_mass(np.inf, 0.0, 0.0, 0.0)


def test_non_numeric_input_raises_error():
    with pytest.raises(ValueError):
        pt("not-a-number", 1.0)