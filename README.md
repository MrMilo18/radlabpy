# radlabpy

**Radiation Laboratory and Particle Physics Analysis in Python**

`radlabpy` is a scientific Python package for reproducible analysis of radiation, detector, nuclear physics, and subnuclear/HEP data.

The package is designed for academic and research-oriented workflows, with emphasis on modularity, reproducibility, validation, testing, and clear documentation.

## Current version

`0.1.0-dev`

## Initial scope

The first development version focuses on:

- radiation counting statistics
- Poisson uncertainties
- count rates
- CPS and CPM conversion
- basic unit-tested functions
- clean package structure using `src/`

Future modules will include:

- spectra analysis
- Gaussian peak fitting
- calibration
- detector analysis
- HEP kinematics
- plotting tools
- basic Machine Learning utilities

## Installation for development

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Radiation analysis utilities

The `radlabpy.radiation` subpackage provides basic tools for radiation counting and spectral analysis.

Current features include:

* Poisson uncertainty calculation for counting experiments.
* Basic counting summaries.
* Count-rate calculations in CPS and CPM.
* Gaussian peak model for simple spectra.
* Gaussian peak fitting with constant background.
* FWHM calculation from Gaussian sigma.
* Relative energy resolution calculation.
* Basic spectrum utilities:

  * total counts,
  * spectrum normalization,
  * peak channel search.

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

A complete example is available in:

```text
examples/spectrum_fit.py
```

Run it with:

```bash
python examples/spectrum_fit.py
```

The project tests can be executed with:

```bash
pytest
```
