# radlabpy User Guide

This user guide provides a short introduction to the current functionality of `radlabpy`.

`radlabpy` is a scientific Python package for reproducible analysis of radiation, detector, nuclear physics, and high-energy physics data. It can be used both as a Python package and through a minimal command-line interface.

## Installation

From the root directory of the project, create and activate a virtual environment:

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

## Python API

The package can be imported from Python scripts, notebooks, or interactive sessions.

Example:

```python
from radlabpy.radiation import counting_summary

counts = [21, 24, 20, 26, 23]

summary = counting_summary(counts)

print(summary)
```

The main current modules are:

```text
radlabpy.radiation
radlabpy.detectors
radlabpy.hep
radlabpy.io
radlabpy.plotting
```

## Command-line interface

`radlabpy` can also be used from the terminal through the `radlab` command.

The command is available after installing the package in editable mode:

```bash
python -m pip install -e .
```

General help:

```bash
radlab --help
```

Package version:

```bash
radlab --version
```

The command-line interface is intended for quick, reproducible analyses from the terminal. It does not replace the Python API; instead, it provides a simple interface to selected package functionality.

## Geiger counting data

Analyze a CSV file with radiation counting data:

```bash
radlab geiger data/geiger_sample.csv
```

Optional column name:

```bash
radlab geiger data/geiger_sample.csv --counts-col counts
```

The input file must contain a column with count measurements. By default, the CLI expects:

```text
counts
```

This command prints a basic statistical summary, including:

```text
number of measurements
mean
standard deviation
minimum
maximum
```

## Radiation spectrum

Analyze a radiation spectrum:

```bash
radlab spectrum data/spectrum_sample.csv
```

With Gaussian peak fitting:

```bash
radlab spectrum data/spectrum_sample.csv --fit-gaussian
```

Optional column names:

```bash
radlab spectrum data/spectrum_sample.csv --channel-col channel --counts-col counts
```

The input file must contain columns compatible with:

```text
channel, counts
```

This command prints:

```text
total counts
peak channel
```

When `--fit-gaussian` is used, it also prints Gaussian fit parameters such as:

```text
amplitude
mean
sigma
FWHM
background
```

## Energy calibration

Run a linear channel-energy calibration:

```bash
radlab calibration data/calibration_sample.csv
```

Optional column names:

```bash
radlab calibration data/calibration_sample.csv --channel-col channel --energy-col energy
```

The input file must contain columns compatible with:

```text
channel, energy
```

The calibration convention is:

```text
E = slope * channel + intercept
```

The command prints:

```text
slope
intercept
R²
residual mean
residual standard deviation
```

## HEP event table

Analyze a simple HEP-like event table:

```bash
radlab hep data/hep_events_sample.csv
```

The event table must include columns compatible with a four-momentum:

```text
E, px, py, pz
```

The invariant mass convention is:

```text
m² = E² - px² - py² - pz²
```

The current implementation uses natural units with:

```text
c = 1
```

Rows with physically inconsistent four-momenta, where `m²` is negative beyond numerical tolerance, are rejected.

The command prints a statistical summary of the invariant masses, including:

```text
number of events
mean mass
standard deviation
minimum mass
maximum mass
```

## Detector data

Analyze simple detector data:

```bash
radlab detector data/detector_sample.csv
```

The detector command automatically detects which calculation can be performed from the available columns.

Currently supported column combinations are:

```text
detected, emitted
counts, time
signal, noise
```

Depending on the available columns, the command computes:

```text
detection efficiency
event rate
signal-to-noise ratio
```

## Sample datasets

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

These files are intentionally small. They are meant for examples, tests, documentation, and quick demonstrations of the package workflow.

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

## Testing

Run the full test suite with:

```bash
pytest
```

The package includes tests for radiation counting, spectrum analysis, Gaussian fitting, calibration, HEP kinematics, detector utilities, input/output, plotting, and the command-line interface.

## Design notes

`radlabpy` follows these design principles:

```text
modular source code organization
separation between calculation, I/O, plotting, tests, and examples
small reusable functions
clear public API
scientific validation
unit-tested functionality
reproducible examples
minimal but useful command-line interface
```

The command-line interface is intentionally simple. More advanced workflows should still use the Python API directly.
