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
