# radlabpy

**Radiation Laboratory and Particle Physics Analysis in Python**

`radlabpy` is a scientific Python package for reproducible analysis of radiation, detector, nuclear physics, and subnuclear/high-energy physics data.

The package is designed for academic and research-oriented workflows, with emphasis on modularity, reproducibility, validation, testing, visualization, and clear documentation.

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
* CSV input/output utilities;
* scientific plotting utilities;
* minimal command-line interface;
* small reproducible sample datasets;
* unit-tested functions;
* clean package structure using `src/`.

Future modules may include:

* automatic peak detection;
* event selection tools;
* basic Machine Learning utilities;
* signal-background classification;
* more advanced command-line interface tools.

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

Current modules and subpackages include:

```text
radlabpy.io
radlabpy.plotting
radlabpy.radiation
radlabpy.hep
radlabpy.detectors
```

The project also includes:

```text
data/
examples/
tests/
docs/
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

## Input/output utilities

The `radlabpy.io` module provides simple CSV-based input/output tools for reproducible examples and small tabular datasets.

Current features include:

* reading generic CSV files;
* reading counting CSV files;
* reading spectrum CSV files;
* reading event tables;
* checking that input files exist;
* checking required columns;
* writing summary dictionaries or tables to CSV.

Available functions include:

```python
from radlabpy.io import (
    read_csv_data,
    read_spectrum_csv,
    read_counting_csv,
    read_event_table,
    write_summary_csv,
)
```

Example:

```python
from radlabpy.io import read_spectrum_csv
from radlabpy.radiation import fit_gaussian_peak

spectrum = read_spectrum_csv("data/spectrum_sample.csv")

channels = spectrum["channel"]
counts = spectrum["counts"]

fit = fit_gaussian_peak(channels, counts)

print(fit)
```

The I/O module is intentionally limited to reading, validating, and writing data. Physics calculations are handled by `radlabpy.radiation`, `radlabpy.hep`, and `radlabpy.detectors`.

## Scientific plotting utilities

The `radlabpy.plotting` module provides publication-friendly Matplotlib plotting functions.

Current plotting functions include:

```python
from radlabpy.plotting import (
    plot_counts_time,
    plot_spectrum,
    plot_gaussian_fit,
    plot_calibration,
    plot_calibration_residuals,
    plot_invariant_mass,
)
```

Design conventions:

* every plotting function returns `fig, ax`;
* functions accept `ax=None` or an existing Matplotlib axis;
* functions do not call `plt.show()` internally;
* functions do not save figures automatically;
* plotting is kept separate from physical calculations;
* labels, titles, grids and annotations can be customized.

Example:

```python
import matplotlib.pyplot as plt

from radlabpy.io import read_spectrum_csv
from radlabpy.plotting import plot_gaussian_fit
from radlabpy.radiation import fit_gaussian_peak

spectrum = read_spectrum_csv("data/spectrum_sample.csv")

channels = spectrum["channel"]
counts = spectrum["counts"]

fit = fit_gaussian_peak(channels, counts)

fig, ax = plot_gaussian_fit(
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
```

To save a figure manually:

```python
fig.savefig("spectrum_fit.png", dpi=300, bbox_inches="tight")
```

## Sample data

The repository includes small reproducible datasets in:

```text
data/
```

Current sample files include:

```text
data/geiger_sample.csv
data/spectrum_sample.csv
data/calibration_sample.csv
data/hep_events_sample.csv
data/detector_sample.csv
```

These files are intentionally small and simple. They are meant for examples, tests, documentation, and quick demonstrations of the package workflow.

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

The current implementation uses natural units with `c = 1`. Energies, momenta and masses must be given in compatible units, for example GeV.

Available observables include:

* transverse momentum `pT`;
* total three-momentum `p`;
* relativistic energy `E`;
* azimuthal angle `phi`;
* pseudorapidity `eta`;
* invariant mass;
* angular separation `Delta R`.

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

## Command-line interface

`radlabpy` includes a minimal command-line interface called `radlab`.

After installing the package in editable mode:

```bash
python -m pip install -e .
```

you can display the general help with:

```bash
radlab --help
```

and check the installed version with:

```bash
radlab --version
```

The CLI is intended for quick, reproducible analyses from the terminal. It does not replace the Python API; instead, it provides a lightweight interface to selected package functionality.

### Geiger counting analysis

Analyze a CSV file with radiation counting data:

```bash
radlab geiger data/geiger_sample.csv
```

You can also specify the name of the counts column:

```bash
radlab geiger data/geiger_sample.csv --counts-col counts
```

This command reads counting data and prints a basic statistical summary including the number of measurements, mean, standard deviation, minimum and maximum counts.

### Spectrum analysis

Analyze a radiation spectrum:

```bash
radlab spectrum data/spectrum_sample.csv
```

Fit a Gaussian peak to the spectrum:

```bash
radlab spectrum data/spectrum_sample.csv --fit-gaussian
```

You can also specify the column names:

```bash
radlab spectrum data/spectrum_sample.csv --channel-col channel --counts-col counts
```

This command prints the total counts, the peak channel and, optionally, Gaussian fit parameters such as amplitude, mean, sigma and FWHM.

### Energy calibration

Run a linear channel-energy calibration:

```bash
radlab calibration data/calibration_sample.csv
```

You can also specify the channel and energy columns:

```bash
radlab calibration data/calibration_sample.csv --channel-col channel --energy-col energy
```

The calibration convention is:

```text
E = slope * channel + intercept
```

The command prints the slope, intercept, coefficient of determination `R²`, and residual statistics.

### HEP invariant mass analysis

Analyze a simple HEP-like event table:

```bash
radlab hep data/hep_events_sample.csv
```

The input file must contain columns compatible with a four-momentum:

```text
E, px, py, pz
```

The command computes invariant masses event by event and prints a statistical summary.

The current convention uses natural units with `c = 1`:

```text
m² = E² - px² - py² - pz²
```

Rows with physically inconsistent four-momenta, where `m²` is negative beyond numerical tolerance, are rejected.

### Detector analysis

Analyze simple detector data:

```bash
radlab detector data/detector_sample.csv
```

The command automatically detects which calculation can be performed from the available columns. Currently supported column combinations are:

```text
detected, emitted
counts, time
signal, noise
```

Depending on the available columns, the command computes detection efficiency, event rate or signal-to-noise ratio.


## Reproducible examples

Current examples include:

```text
examples/geiger_analysis.py
examples/spectrum_fit.py
examples/energy_calibration.py
examples/invariant_mass_demo.py
examples/detector_analysis.py
```

Run all examples manually from the project root with:

```bash
python examples/geiger_analysis.py
python examples/spectrum_fit.py
python examples/energy_calibration.py
python examples/invariant_mass_demo.py
python examples/detector_analysis.py
```

Some examples open Matplotlib windows. Close the figures to let the scripts finish.

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
tests/test_io.py
tests/test_plotting.py
```

## Design principles

`radlabpy` follows these principles:

* modular source code organization;
* separation between calculation, input/output, visualization, tests and examples;
* small reusable functions;
* clear public API through modules and subpackage `__init__.py` files;
* physically meaningful validation tests;
* readable docstrings;
* reproducible examples;
* development inside a virtual environment;
* publication-friendly scientific visualization.

## Roadmap

### Version 0.1.0

* Initial package structure.
* Radiation counting utilities.
* Basic spectrum analysis.
* Gaussian peak fitting.
* Linear energy calibration.
* Basic detector analysis.
* Basic HEP kinematics.
* CSV input/output utilities.
* Scientific plotting functions.
* Unit tests.
* Minimal reproducible datasets.
* Runnable examples.
* README documentation.

### Version 0.2.0

* Improved spectral analysis.
* Automatic peak detection.
* More detector utilities.
* Event selection tools.
* More examples and notebooks.
* Initial command-line interface.

### Version 0.3.0

* More realistic HEP data support.
* Optional `uproot` integration.
* Advanced histogram utilities.
* Examples with open data.
* Basic Machine Learning utilities.

### Future versions

* Signal-background classification.
* Anomaly detection.
* Optional integration with more professional HEP workflows.
* Optional ROOT-oriented workflows through `uproot`.
