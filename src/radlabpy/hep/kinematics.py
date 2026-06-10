"""
Basic relativistic kinematics utilities for high-energy physics.

This module provides tools for simple HEP observables such as transverse
momentum, pseudorapidity, azimuthal angle, invariant mass and angular
separation Delta R.

Conventions
-----------
Natural units are used, with c = 1.

Energies, momenta and masses must be given in compatible units,
for example GeV.

The relativistic energy convention is:

    E = sqrt(px^2 + py^2 + pz^2 + m^2)

The invariant mass convention is:

    m^2 = E^2 - px^2 - py^2 - pz^2
"""
from __future__ import annotations

import numpy as np

def _as_array(values, name: str = "values"):
    """
    Convert input values to a NumPy array with float dtype.

    Parameters
    ----------
    values : float, int, list, tuple, or array-like
        Input numerical values.
    name : str
        Name used in error messages.
    """
    try:
        return np.asarray(values, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must contain numeric values.") from exc
    
def _validate_finite(values, name:str = "values") -> None:
    """
    Validate that all values are finite numbers.

    Parameters
    ----------
    values : array-like
        Values to validate.
    name : str
        Name used in error messages.

    """

    array = _as_array(values, name=name)

    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values.")
    

def _return_sacalar_if_scalar(result):
    """
    Return a Python float if the result is scalar-like.

    Otherwise, return the NumPy array.
    """
    result = np.asarray(result, dtype=float)

    if result.ndim == 0:
        return float(result)
    
    return result

def pt(px, py):
    """
    Calculate transverse momentum.

    The transverse momentum is defined as:

        pT = sqrt(px^2 + py^2)

    Parameters
    ----------
    px, py : float, int, list, tuple, or array-like
        Momentum components in compatible units, for example Gev.

    Returns
    -------
    float or numpy.ndarray
        Transverse momentum
    """
    px_array = _as_array(px, name="px")
    py_array = _as_array(py, name="py")

    _validate_finite(px_array, name="px")
    _validate_finite(py_array, name="py")

    result = np.sqrt(px_array**2 + py_array**2)

    return _return_sacalar_if_scalar(result)

def momentum(px, py, pz):
    """
    Calculate the magnitude of the three-momentum.

    The momentum magnitude is defined as:

        p = sqrt(px^2 + py^2 + pz^2)

    Parameters
    ----------
    px, py, pz : float, int, list, tuple, or array-like
        Momentum components in compatible units, for example GeV.
    
    Returns
    -------
    float or numpy.ndarray
        Magnitude of the three-momentum.
    """
    px_array = _as_array(px, name="px")
    py_array = _as_array(py, name="py")
    pz_array = _as_array(pz, name="pz")

    _validate_finite(px_array, name="px")
    _validate_finite(py_array, name="py")
    _validate_finite(pz_array, name="pz")

    result = np.sqrt(px_array**2 + py_array**2 + pz_array**2)

    return _return_sacalar_if_scalar(result)

def energy(px, py, pz, mass):
    """
    Calculate relativistic energy in natural units.

    The energy is defined as:

        E = sqrt(px^2 + py^2 + pz^2 + m^2)

    Parameters
    ----------
    px, py, pz : float, int, list, tuple, or array-like
        Momentum components in compatible units, for example GeV.
    mass : float, int, list, tuple, or array-like
        Rest mass in compatible units, for example GeV.

    Returns
    -------
    float or numpy.ndarray
        Relativistic energy.

    """
    px_array = _as_array(px, name="px")
    py_array = _as_array(py, name="py")
    pz_array = _as_array(pz, name="pz")
    mass_array = _as_array(mass, name="mass")

    _validate_finite(px_array, name="px")
    _validate_finite(py_array, name="py")
    _validate_finite(pz_array, name="pz")
    _validate_finite(mass_array, name="mass")

    if np.any(mass_array < 0):
        raise ValueError("mass must be non-negative")
    
    result = np.sqrt(px_array**2 + py_array**2 + pz_array**2 + mass_array**2)

    return _return_sacalar_if_scalar(result)

def phi(px, py):
    """
    Calculate the azimuthal angle phi.

    The angle is calculated using:

        phi = arctan2(py, px)

    Parameters
    ----------
    px, py : float, int, list, tuple, or array-like
        Transverse momentum components.

    Returns
    -------
    float or numpy.ndarray
        Azimuthal angle in radians, in the interval [-pi, pi].
    
    """
    px_array = _as_array(px, name="px")
    py_array = _as_array(py, name="py")

    _validate_finite(px_array, name="px")
    _validate_finite(py_array, name="py")

    result = np.arctan2(py_array, px_array)

    return _return_sacalar_if_scalar(result)

def eta(px, py, pz):
    """
    Calculate pseudorapidity.

    The pseudorapidity is defined as:

        eta = 0.5 * ln((p + pz) / (p - pz))

    where:

        p = sqrt(px^2 + py^2 + pz^2)

    Parameters
    ----------
    px, py, pz : float, int, list, tuple, or array-like
        Momentum components in compatible units.

    Returns
    -------
    float or numpy.ndarray
        Pseudorapidity. The result can be positive or negative infinity for
        particles exactly along the beam axis.
    """
    px_array = _as_array(px, name="px")
    py_array = _as_array(py, name="py")
    pz_array = _as_array(pz, name="pz")

    _validate_finite(px_array, name="px")
    _validate_finite(py_array, name="py")
    _validate_finite(pz_array, name="pz")

    p_array = np.sqrt(px_array**2 + py_array**2 + pz_array**2)

    if np.any(p_array == 0):
        raise ValueError("pseudorapidity is undefined for zero momentum.")
    
    with np.errstate(divide="ignore", invalid="ignore"):
        result = 0.5 * np.log((p_array + pz_array) / (p_array - pz_array))

    return _return_sacalar_if_scalar(result)

def invariant_mass(E, px, py, pz, tolerance: float = 1e-12):
    """
    Calculate invariant mass from a four-momentum.

    The invariant mass is calculated using:

        m^2 = E^2 - px^2 - py^2 - pz^2
    
    Parameters
    ----------
    E : float, int, list, tuple, or array-like
        Energy in compatible units, for example GeV.
    px, py, pz : float, int, list, tuple, or array-like
        Momentum components in compatible units, for example GeV.
    tolerance : float, optional
        Numerical tolerance for small negative values of m^2 caused by
        floating-point roundoff. Default is 1e-12.
    
    Returns
    -------
    float o numpy.ndarray
        Invariant mass.
    
    """
    E_array = _as_array(E, name="E")
    px_array = _as_array(px, name="px")
    py_array = _as_array(py, name="py")
    pz_array = _as_array(pz, name="pz")

    _validate_finite(E_array, name="E")
    _validate_finite(px_array, name="px")
    _validate_finite(py_array, name="py")
    _validate_finite(pz_array, name="pz")

    if tolerance < 0:
        raise ValueError("tolerance must be non-negative.")
    
    if np.any(E_array < 0):
        raise ValueError("E must be non-negative.")
    
    mass_squared = E_array**2 - px_array**2 - py_array**2 - pz_array**2 

    if np.any(mass_squared < -tolerance):
        raise ValueError(
            "invariant mass squared is negative beyond numerical tolerance."
        )
    
    mass_squared = np.where(mass_squared < 0.0, 0.0, mass_squared)
    result = np.sqrt(mass_squared)

    return _return_sacalar_if_scalar(result)

def delta_phi(phi1, phi2):
    """
    Calculate angular separation in phi.

    The pariodicity of the azimuthal angle is handled so that the result
    lies in the interval [-pi, pi]:

        Delta phi = (phi1 - phi2 + pi) mod 2pi - pi

    Parameters
    ----------
    phi1, phi2 : float, int, list, tuple, or array-like
        Azimuthal angles in radians.

    Returns
    -------
    float or numpy.ndarray
        Angular difference in radians.       
    """
    phi1_array = _as_array(phi1, name="phi1")
    phi2_array = _as_array(phi2, name="phi2")

    _validate_finite(phi1_array, name="phi1")
    _validate_finite(phi2_array, name="phi2")

    result = (phi1_array - phi2_array + np.pi) % (2.0 * np.pi) - np.pi

    return _return_sacalar_if_scalar(result)

def delta_r(eta1, phi1, eta2, phi2):
    """
    Calculate angular separation Delta R.

    The angular separation is defined as:

        Delta R = sqrt((eta1 - eta2)^2 + Delta phi^2)

    Parameters
    ----------
    eta1, phi1, eta2, phi2 : float, int, list, tuple, or array-like
        Pseudorapidities and azimuthal angles.

    Returns
    -------
    float or numpy.ndarray
        Angular separation Delta R.
    """    

    eta1_array = _as_array(eta1, name="eta1")
    eta2_array = _as_array(eta2, name="eta2")

    _validate_finite(eta1_array, name="eta1")
    _validate_finite(eta2_array, name="eta2")

    d_eta = eta1_array - eta2_array
    d_phi = delta_phi(phi1, phi2)

    result = np.sqrt(d_eta**2 + np.asarray(d_phi, dtype=float)**2)

    return _return_sacalar_if_scalar(result)