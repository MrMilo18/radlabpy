# radlabpy

**Radiation Laboratory and Particle Physics Analysis in Python**

`radlabpy` is a scientific Python package for reproducible analysis of radiation, detector, nuclear physics, and subnuclear/high-energy physics data.

The package is designed for academic and research-oriented workflows, with emphasis on modularity, reproducibility, scientific validation, testing, visualization, and clear documentation.

---

## Current version

```text
0.1.0
```

Version `0.1.0` is the first stable academic release of `radlabpy`.

This release focuses on a solid, tested, and documented scientific core. Machine Learning was considered in the original project design, but it is intentionally left for a future version.

---

## Main features

The current version includes tools for:

* radiation counting statistics;
* Poisson uncertainties;
* count-rate calculations;
* CPS and CPM conversion;
* spectrum utilities;
* Gaussian peak modeling and fitting;
* FWHM and relative energy resolution;
* linear energy calibration;
* basic high-energy physics kinematics;
* basic detector efficiency and rate analysis;
* coincidence and accidental coincidence calculations;
* signal-to-noise ratio;
* CSV input/output utilities;
* scientific plotting utilities;
* command-line interface through `radlab`;
* reproducible sample datasets;
* unit tests with `pytest`.

---

## Project scope

`radlabpy` is intended as a compact but extensible scientific package for educational and introductory research workflows involving:

* radiation counting experiments;
* Geiger counter data;
* simple alpha/gamma spectrum analysis;
* detector characterization;
* energy calibration;
* HEP-like four-vector tables;
* invariant mass calculations;
* reproducible command-line analyses.

This version does not attempt to replace specialized software such as ROOT, Geant4, or full HEP analysis frameworks. Instead, it provides a clean Python foundation for learning, testing, and extending scientific analysis workflows.

---

## Installation for development

Clone the repository:

```bash
git clone <repository-url>
cd radlabpy
```

Create and activate a virtual environment.

On Linux or WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Upgrade `pip`:

```bash
python -m pip install --upgrade pip
```

Install the package in editable mode:

```bash
python -m pip install -e .
```

Editable installation is recommended during development because changes in `src/radlabpy/` are immediately reflected without reinstalling the package.

---

## Dependencies

The main dependencies are:

```text
numpy
scipy
pandas
matplotlib
pytest
```

They are listed in `requirements.txt` and in the project configuration.

To install dependencies manually:

```bash
python -m pip install -r requirements.txt
```

---

## Quick test

After installation, verify that the package works:

```bash
pytest
```

You can also check the command-line interface:

```bash
radlab --help
radlab --version
```

---

## Package structure

The repository follows a standard scientific Python package structure using `src/`:

```text
radlabpy/
├── README.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── data/
│   ├── calibration_sample.csv
│   ├── detector_sample.csv
│   ├── geiger_sample.csv
│   ├── hep_events_sample.csv
│   └── spectrum_sample.csv
├── docs/
│   └── user_guide.md
├── examples/
│   ├── detector_analysis.py
│   ├── energy_calibration.py
│   ├── geiger_analysis.py
│   ├── invariant_mass_demo.py
│   └── spectrum_fit.py
├── src/
│   └── radlabpy/
│       ├── __init__.py
│       ├── cli.py
│       ├── io.py
│       ├── plotting.py
│       ├── radiation/
│       │   ├── __init__.py
│       │   ├── counting.py
│       │   ├── fitting.py
│       │   ├── spectra.py
│       │   └── calibration.py
│       ├── detectors/
│       │   ├── __init__.py
│       │   ├── coincidence.py
│       │   ├── efficiency.py
│       │   ├── rates.py
│       │   └── signals.py
│       └── hep/
│           ├── __init__.py
│           └── kinematics.py
└── tests/
    ├── test_calibration.py
    ├── test_cli.py
    ├── test_counting.py
    ├── test_detectors.py
    ├── test_fitting.py
    ├── test_io.py
    ├── test_kinematics.py
    ├── test_plotting.py
    └── test_spectra.py
```

---

## Python API

`radlabpy` can be used from Python scripts, notebooks, or interactive sessions.

### Radiation counting

```python
from radlabpy.radiation import (
    poisson_uncertainty,
    counting_summary,
    count_rate,
    cps_to_cpm,
    cpm_to_cps,
)

counts = [21, 24, 20, 26, 23]

summary = counting_summary(counts)
uncertainty = poisson_uncertainty(100)
rate = count_rate(counts=1200, time=60.0)

print(summary)
print(uncertainty)
print(rate)
```

---

### Spectrum analysis and Gaussian fitting

```python
import numpy as np

from radlabpy.radiation import (
    gaussian,
    fit_gaussian_peak,
    fwhm_from_sigma,
    energy_resolution,
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

---

### Spectrum utilities

```python
from radlabpy.radiation import (
    total_counts,
    normalize_spectrum,
    find_peak_channel,
)

channels = [0, 1, 2, 3, 4]
counts = [1, 5, 12, 6, 2]

total = total_counts(counts)
normalized = normalize_spectrum(counts)
peak = find_peak_channel(channels, counts)

print(total)
print(normalized)
print(peak)
```

---

### Energy calibration

The linear calibration convention is:

```text
E = slope * channel + intercept
```

Example:

```python
from radlabpy.radiation import (
    linear_calibration,
    channel_to_energy,
    energy_to_channel,
    calibration_residuals,
)

channels = [100, 200, 300, 400]
energies = [0.5, 1.0, 1.5, 2.0]

calibration = linear_calibration(channels, energies)

energy = channel_to_energy(250, calibration)
channel = energy_to_channel(1.25, calibration)
residuals = calibration_residuals(channels, energies, calibration)

print(calibration)
print(energy)
print(channel)
print(residuals)
```

---

### Detector analysis

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

eff = detection_efficiency(detected=850, emitted=1000)
eff_unc = efficiency_uncertainty(detected=850, emitted=1000)

rate = event_rate(counts=1200, time=60.0)
rate_unc = rate_uncertainty(counts=1200, time=60.0)

coinc = coincidence_rate(coincidences=180, time=60.0)

acc = accidental_coincidence_rate(
    rate1=25.0,
    rate2=30.0,
    coincidence_window=100e-9,
)

snr = signal_to_noise(signal=50.0, noise=5.0)

print(eff, eff_unc)
print(rate, rate_unc)
print(coinc)
print(acc)
print(snr)
```

---

### High-energy physics kinematics

The HEP module uses natural units with:

```text
c = 1
```

The main conventions are:

```text
E = sqrt(px^2 + py^2 + pz^2 + m^2)
m^2 = E^2 - px^2 - py^2 - pz^2
Delta R = sqrt((eta1 - eta2)^2 + Delta phi^2)
```

Example:

```python
from radlabpy.hep import (
    pt,
    momentum,
    energy,
    phi,
    eta,
    invariant_mass,
    delta_phi,
    delta_r,
)

px = 3.0
py = 4.0
pz = 0.0
mass = 2.0

pT = pt(px, py)
p = momentum(px, py, pz)
E = energy(px, py, pz, mass)
m = invariant_mass(E, px, py, pz)

print(f"pT = {pT:.3f}")
print(f"p = {p:.3f}")
print(f"E = {E:.3f}")
print(f"m = {m:.3f}")
```

---

## Input/output utilities

The `radlabpy.io` module provides simple CSV-based tools for reproducible examples and small tabular datasets.

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

The I/O module is intentionally limited to reading, validating, and writing data. Physics calculations are handled by the `radiation`, `detectors`, and `hep` subpackages.

---

## Plotting utilities

The `radlabpy.plotting` module provides Matplotlib-based plotting functions.

Available functions include:

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

* plotting functions return `fig, ax`;
* functions accept `ax=None` or an existing Matplotlib axis;
* functions do not call `plt.show()` internally;
* functions do not save figures automatically;
* plotting is separated from physical calculations;
* figures can be customized and saved by the user.

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

---

## Command-line interface

`radlabpy` includes a command-line interface called `radlab`.

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

---

### Geiger counting analysis

Analyze a CSV file with radiation counting data:

```bash
radlab geiger data/geiger_sample.csv
```

Specify the counts column:

```bash
radlab geiger data/geiger_sample.csv --counts-col counts
```

This command reads counting data and prints a basic statistical summary.

---

### Spectrum analysis

Analyze a radiation spectrum:

```bash
radlab spectrum data/spectrum_sample.csv
```

Fit a Gaussian peak:

```bash
radlab spectrum data/spectrum_sample.csv --fit-gaussian
```

Specify custom column names:

```bash
radlab spectrum data/spectrum_sample.csv --channel-col channel --counts-col counts
```

This command prints the total counts, peak channel and, optionally, Gaussian fit parameters.

---

### Energy calibration

Run a linear channel-energy calibration:

```bash
radlab calibration data/calibration_sample.csv
```

Specify custom columns:

```bash
radlab calibration data/calibration_sample.csv --channel-col channel --energy-col energy
```

The calibration convention is:

```text
E = slope * channel + intercept
```

The command prints the slope, intercept, coefficient of determination `R²`, and residual statistics.

---

### HEP invariant mass analysis

Analyze a simple HEP-like event table:

```bash
radlab hep data/hep_events_sample.csv
```

The input file must contain:

```text
E, px, py, pz
```

The command computes invariant masses event by event and prints a statistical summary.

The invariant mass convention is:

```text
m² = E² - px² - py² - pz²
```

Rows with physically inconsistent four-momenta, where `m²` is negative beyond numerical tolerance, are rejected.

---

### Detector analysis

Analyze simple detector data:

```bash
radlab detector data/detector_sample.csv
```

The command automatically detects which calculation can be performed from the available columns.

Currently supported column combinations are:

```text
detected, emitted
counts, time
signal, noise
```

Depending on the available columns, the command computes detection efficiency, event rate or signal-to-noise ratio.

---

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

---

## Reproducible examples

Runnable Python examples are available in:

```text
examples/
```

Current examples include:

```text
examples/geiger_analysis.py
examples/spectrum_fit.py
examples/energy_calibration.py
examples/invariant_mass_demo.py
examples/detector_analysis.py
```

Run them from the project root with:

```bash
python examples/geiger_analysis.py
python examples/spectrum_fit.py
python examples/energy_calibration.py
python examples/invariant_mass_demo.py
python examples/detector_analysis.py
```

Some examples may open Matplotlib windows. Close the figures to let the scripts finish.

---

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
tests/test_cli.py
```

The tests verify numerical behavior, input validation, physical consistency and command-line execution.

---

## Scientific conventions

The current version uses the following conventions.

### Counting statistics

For Poisson-distributed counts:

```text
sigma_N = sqrt(N)
```

### Count rate

```text
rate = counts / time
```

### Gaussian FWHM

```text
FWHM = 2 * sqrt(2 * ln(2)) * sigma
```

### Energy resolution

```text
R = FWHM / E
```

### Linear calibration

```text
E = slope * channel + intercept
```

### Relativistic kinematics

Natural units are used:

```text
c = 1
```

with:

```text
E = sqrt(px^2 + py^2 + pz^2 + m^2)
m^2 = E^2 - px^2 - py^2 - pz^2
```

### Angular separation

```text
Delta R = sqrt((eta1 - eta2)^2 + Delta phi^2)
```

---

## Documentation

Additional documentation is available in:

```text
docs/user_guide.md
```

Recommended future documentation files:

```text
docs/api_reference.md
docs/validation.md
```

The user guide provides a compact introduction to installation, Python usage, CLI usage, sample datasets, examples and tests.

---

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
* installation in editable mode during development;
* publication-friendly scientific visualization;
* command-line tools for quick reproducible workflows.

---

## Roadmap

### Version 0.1.0

Implemented:

* initial package structure;
* radiation counting utilities;
* basic spectrum analysis;
* Gaussian peak fitting;
* linear energy calibration;
* basic detector analysis;
* basic HEP kinematics;
* CSV input/output utilities;
* scientific plotting functions;
* command-line interface;
* unit tests;
* minimal reproducible datasets;
* runnable examples;
* README and user guide.

### Version 0.2.0

Possible future improvements:

* automatic peak detection;
* improved spectrum preprocessing;
* additional detector utilities;
* more CLI options;
* richer validation examples;
* extended documentation;
* example notebooks.

### Version 0.3.0 and later

Possible future extensions:

* optional support for ROOT-like data through `uproot`;
* more realistic HEP event workflows;
* histogram utilities;
* event selection tools;
* uncertainty propagation tools;
* advanced fitting routines;
* larger example datasets.

### Future Machine Learning module

Machine Learning is intentionally left for a future version.

Possible future ML features:

* signal-background classification;
* spectrum feature extraction;
* anomaly detection in counting data;
* classification of HEP-like events;
* interpretable models based on physical observables;
* evaluation metrics beyond accuracy.

---

## Academic status

`radlabpy` version `0.1.0` is an academic scientific software project focused on clean design, reproducibility, testing and documentation.

It is suitable for demonstrating:

* package structure in Python;
* scientific programming practices;
* modular analysis workflows;
* reproducible examples;
* unit testing;
* command-line tools;
* documentation of physical and numerical conventions.

---

## Author

**Emilio Rodríguez**
Facultad de Ciencias, UNAM

---

## License

This project is intended for academic and educational use.

A formal open-source license may be added in a future release.
