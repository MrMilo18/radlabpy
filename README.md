# radlabpy

**Radiation Laboratory and Particle Physics Analysis in Python**

`radlabpy` is a scientific Python package for reproducible analysis of radiation, detector, nuclear physics, and subnuclear/high-energy physics data.

The package is designed for academic and research-oriented workflows, with emphasis on modularity, reproducibility, validation, testing, and clear documentation.

## Current version

`0.1.0-dev`

## Current development scope

The current development version includes:

* radiation counting statistics;
* Poisson uncertainties;
* count rates;
* CPS and CPM conversion;
* basic spectrum utilities;
* Gaussian peak modeling and fitting;
* FWHM and relative energy resolution;
* linear energy calibration;
* basic high-energy physics kinematics;
* basic detector analysis utilities;
* unit-tested functions;
* clean package structure using `src/`.

Future modules may include:

* plotting tools;
* automatic peak detection;
* event selection tools;
* basic Machine Learning utilities;
* signal-background classification;
* simple command-line interface tools.

## Installation for development

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the package in editable mode:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

Run the test suite with:

```bash
pytest
```

## Package structure

The main source code lives inside:

```text
src/radlabpy/
```

Current subpackages include:

```text
radlabpy.radiation
radlabpy.hep
radlabpy.detectors
```

## Radiation analysis utilities

The `radlabpy.radiation` subpackage provides basic tools for radiation counting and spectral analysis.

Current features include:

* Poisson uncertainty calculation for counting experiments;
* basic counting summaries;
* count-rate calculations;
* CPS and CPM conversion;
* Gaussian peak model for simple spectra;
* Gaussian peak fitting with constant background;
* FWHM calculation from Gaussian sigma;
* relative energy resolution calculation;
* total counts in a spectrum;
* spectrum normalization;
* peak channel search;
* linear channel-energy calibration.

Example:

```python
import numpy as np

from radlabpy.radiation import (
    fit_gaussian_peak,
    fwhm_from_sigma,
    energy_resolution,
    gaussian,
)

channels = np.linspace(0.0, 200.0, 401)

counts = gaussian(
    channels,
    amplitude=500.0,
    mean=100.0,
    sigma=8.0,
    background=25.0,
)

fit = fit_gaussian_peak(channels, counts)

fwhm = fwhm_from_sigma(fit["sigma"])
resolution = energy_resolution(fwhm, fit["mean"])

print(fit)
print(f"FWHM: {fwhm:.3f}")
print(f"Resolution: {resolution:.4f}")
```

Complete radiation examples are available in:

```text
examples/geiger_analysis.py
examples/spectrum_fit.py
examples/energy_calibration.py
```

Run them with:

```bash
python examples/geiger_analysis.py
python examples/spectrum_fit.py
python examples/energy_calibration.py
```

## Detector analysis utilities

The `radlabpy.detectors` subpackage provides basic tools for detector analysis.

Current features include:

* detection efficiency;
* approximate binomial efficiency uncertainty;
* event rates;
* Poisson rate uncertainties;
* coincidence rates;
* accidental coincidence rates for two independent channels;
* signal-to-noise ratio.

Available functions include:

```python
from radlabpy.detectors import (
    detection_efficiency,
    efficiency_uncertainty,
    event_rate,
    rate_uncertainty,
    coincidence_rate,
    accidental_coincidence_rate,
    signal_to_noise,
)
```

Example:

```python
from radlabpy.detectors import (
    detection_efficiency,
    efficiency_uncertainty,
    event_rate,
    rate_uncertainty,
    coincidence_rate,
    accidental_coincidence_rate,
    signal_to_noise,
)

detected = 850
emitted = 1000

efficiency = detection_efficiency(detected, emitted)
sigma_efficiency = efficiency_uncertainty(detected, emitted)

counts = 1200
time = 60.0

rate = event_rate(counts, time)
sigma_rate = rate_uncertainty(counts, time)

coincidences = 180
coincidence = coincidence_rate(coincidences, time)

rate1 = 25.0
rate2 = 30.0
coincidence_window = 100e-9

accidental = accidental_coincidence_rate(
    rate1,
    rate2,
    coincidence_window,
)

snr = signal_to_noise(signal=50.0, noise=5.0)

print(f"Efficiency: {efficiency:.4f} ± {sigma_efficiency:.4f}")
print(f"Event rate: {rate:.4f} ± {sigma_rate:.4f} counts/s")
print(f"Coincidence rate: {coincidence:.4f} coincidences/s")
print(f"Accidental coincidence rate: {accidental:.6e} Hz")
print(f"Signal-to-noise ratio: {snr:.4f}")
```

A complete runnable detector example is available in:

```text
examples/detector_analysis.py
```

Run it with:

```bash
python examples/detector_analysis.py
```

## High-energy physics kinematics

The `radlabpy.hep` subpackage provides basic high-energy physics kinematics utilities.

The current implementation uses natural units with (c = 1). Energies, momenta and masses must be given in compatible units, for example GeV.

Available observables include:

* transverse momentum (p_T);
* total three-momentum (p);
* relativistic energy (E);
* azimuthal angle (\phi);
* pseudorapidity (\eta);
* invariant mass;
* angular separation (\Delta R).

Example:

```python
from radlabpy.hep import energy, invariant_mass, pt

px = 3.0
py = 4.0
pz = 0.0
mass = 2.0

pT = pt(px, py)
E = energy(px, py, pz, mass)
m = invariant_mass(E, px, py, pz)

print(f"pT = {pT:.3f}")
print(f"E = {E:.3f}")
print(f"m = {m:.3f}")
```

A complete runnable HEP example is available in:

```text
examples/invariant_mass_demo.py
```

Run it with:

```bash
python examples/invariant_mass_demo.py
```

## Testing

All implemented modules include unit tests.

Run the full test suite with:

```bash
pytest
```

Current test files include:

```text
tests/test_counting.py
tests/test_fitting.py
tests/test_spectra.py
tests/test_calibration.py
tests/test_kinematics.py
tests/test_detectors.py
```

## Design principles

`radlabpy` follows these principles:

* modular source code organization;
* separation between calculation, input/output, visualization and examples;
* small reusable functions;
* clear public API through subpackage `__init__.py` files;
* physically meaningful validation tests;
* readable docstrings;
* reproducible examples;
* development inside a virtual environment.

## Roadmap

### Version 0.1.0

* Initial package structure.
* Radiation counting utilities.
* Basic spectrum analysis.
* Gaussian peak fitting.
* Linear energy calibration.
* Basic detector analysis.
* Basic HEP kinematics.
* Unit tests.
* Minimal examples.
* README documentation.

### Version 0.2.0

* Improved spectral analysis.
* Automatic peak detection.
* More detector utilities.
* Plotting functions.
* More examples and notebooks.

### Version 0.3.0

* More realistic HEP data support.
* Optional `uproot` integration.
* Advanced histogram utilities.
* Examples with open data.

### Future versions

* Basic Machine Learning utilities.
* Signal-background classification.
* Anomaly detection.
* Optional integration with more professional HEP workflows.
