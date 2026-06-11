# API Reference

This document summarizes the public API available in `radlabpy` version `0.1.0`.

`radlabpy` is organized into focused modules for radiation analysis, detector utilities, high-energy physics kinematics, input/output, plotting, and command-line usage.

---

## Package layout

```text
radlabpy
├── radiation
├── detectors
├── hep
├── io
├── plotting
└── cli
```

---

## `radlabpy.radiation`

The `radiation` subpackage contains tools for radiation counting, spectrum analysis, Gaussian fitting, and energy calibration.

---

### Counting utilities

Module:

```text
radlabpy.radiation.counting
```

Available functions:

```python
poisson_uncertainty(counts)
counting_summary(counts)
count_rate(counts, time)
cps_to_cpm(cps)
cpm_to_cps(cpm)
```

#### `poisson_uncertainty(counts)`

Computes the Poisson statistical uncertainty:

```text
sigma_N = sqrt(N)
```

Parameters:

```text
counts : float, int, list, tuple, or array-like
```

Returns:

```text
float or numpy.ndarray
```

Example:

```python
from radlabpy.radiation import poisson_uncertainty

sigma = poisson_uncertainty(100)
print(sigma)
```

---

#### `counting_summary(counts)`

Computes a basic statistical summary of count measurements.

Returns a dictionary containing:

```text
n_measurements
total_counts
mean_counts
std_counts
min_counts
max_counts
poisson_uncertainty_mean
```

Example:

```python
from radlabpy.radiation import counting_summary

counts = [21, 24, 20, 26, 23]
summary = counting_summary(counts)

print(summary)
```

---

#### `count_rate(counts, time)`

Computes the count rate:

```text
rate = counts / time
```

Example:

```python
from radlabpy.radiation import count_rate

rate = count_rate(1200, 60.0)
print(rate)
```

---

#### `cps_to_cpm(cps)`

Converts counts per second to counts per minute:

```text
CPM = 60 * CPS
```

---

#### `cpm_to_cps(cpm)`

Converts counts per minute to counts per second:

```text
CPS = CPM / 60
```

---

### Spectrum utilities

Module:

```text
radlabpy.radiation.spectra
```

Available functions:

```python
total_counts(counts)
normalize_spectrum(counts)
find_peak_channel(channels, counts)
```

#### `total_counts(counts)`

Returns the total number of counts in a spectrum.

Example:

```python
from radlabpy.radiation import total_counts

counts = [1, 5, 12, 6, 2]
total = total_counts(counts)

print(total)
```

---

#### `normalize_spectrum(counts)`

Normalizes a spectrum so that the sum of all bins is 1.

Example:

```python
from radlabpy.radiation import normalize_spectrum

counts = [1, 5, 12, 6, 2]
normalized = normalize_spectrum(counts)

print(normalized)
```

---

#### `find_peak_channel(channels, counts)`

Finds the channel corresponding to the maximum count value.

Example:

```python
from radlabpy.radiation import find_peak_channel

channels = [0, 1, 2, 3, 4]
counts = [1, 5, 12, 6, 2]

peak = find_peak_channel(channels, counts)
print(peak)
```

---

### Gaussian fitting utilities

Module:

```text
radlabpy.radiation.fitting
```

Available functions:

```python
gaussian(x, amplitude, mean, sigma, background=0.0)
fwhm_from_sigma(sigma)
energy_resolution(fwhm, energy)
estimate_peak_area(amplitude, sigma)
fit_gaussian_peak(x, y)
```

#### `gaussian(x, amplitude, mean, sigma, background=0.0)`

Evaluates a Gaussian function with constant background:

```text
y = amplitude * exp(-(x - mean)^2 / (2 sigma^2)) + background
```

---

#### `fwhm_from_sigma(sigma)`

Computes the full width at half maximum of a Gaussian peak:

```text
FWHM = 2 * sqrt(2 * ln(2)) * sigma
```

---

#### `energy_resolution(fwhm, energy)`

Computes the relative energy resolution:

```text
R = FWHM / E
```

---

#### `estimate_peak_area(amplitude, sigma)`

Estimates the area under a Gaussian peak:

```text
area = amplitude * sigma * sqrt(2*pi)
```

---

#### `fit_gaussian_peak(x, y)`

Fits a Gaussian peak with constant background.

Returns a dictionary containing:

```text
amplitude
mean
sigma
background
```

Example:

```python
from radlabpy.io import read_spectrum_csv
from radlabpy.radiation import fit_gaussian_peak, fwhm_from_sigma

spectrum = read_spectrum_csv("data/spectrum_sample.csv")

channels = spectrum["channel"]
counts = spectrum["counts"]

fit = fit_gaussian_peak(channels, counts)
fwhm = fwhm_from_sigma(fit["sigma"])

print(fit)
print(fwhm)
```

---

### Energy calibration utilities

Module:

```text
radlabpy.radiation.calibration
```

Available functions:

```python
linear_calibration(channels, energies)
channel_to_energy(channels, calibration)
energy_to_channel(energies, calibration)
calibration_residuals(channels, energies, calibration)
```

#### `linear_calibration(channels, energies)`

Fits a linear channel-energy calibration:

```text
E = slope * channel + intercept
```

Returns a dictionary containing:

```text
slope
intercept
r_value
r_squared
```

Example:

```python
from radlabpy.radiation import linear_calibration

channels = [100, 200, 300, 400]
energies = [0.5, 1.0, 1.5, 2.0]

calibration = linear_calibration(channels, energies)
print(calibration)
```

---

#### `channel_to_energy(channels, calibration)`

Converts detector channels to energy values using a calibration dictionary.

---

#### `energy_to_channel(energies, calibration)`

Converts energies to detector channels using a calibration dictionary.

---

#### `calibration_residuals(channels, energies, calibration)`

Computes residuals:

```text
residual = observed_energy - calibrated_energy
```

---

## `radlabpy.detectors`

The `detectors` subpackage contains basic detector analysis utilities.

Available functions:

```python
detection_efficiency(detected, emitted)
efficiency_uncertainty(detected, emitted)
event_rate(counts, time)
rate_uncertainty(counts, time)
coincidence_rate(coincidences, time)
accidental_coincidence_rate(rate1, rate2, coincidence_window)
signal_to_noise(signal, noise)
```

---

### Efficiency utilities

Module:

```text
radlabpy.detectors.efficiency
```

#### `detection_efficiency(detected, emitted)`

Computes:

```text
efficiency = detected / emitted
```

---

#### `efficiency_uncertainty(detected, emitted)`

Computes the approximate binomial uncertainty:

```text
sigma_eff = sqrt(efficiency * (1 - efficiency) / emitted)
```

---

### Rate utilities

Module:

```text
radlabpy.detectors.rates
```

#### `event_rate(counts, time)`

Computes:

```text
rate = counts / time
```

---

#### `rate_uncertainty(counts, time)`

Computes the Poisson uncertainty of an event rate:

```text
sigma_rate = sqrt(counts) / time
```

---

### Coincidence utilities

Module:

```text
radlabpy.detectors.coincidence
```

#### `coincidence_rate(coincidences, time)`

Computes:

```text
coincidence_rate = coincidences / time
```

---

#### `accidental_coincidence_rate(rate1, rate2, coincidence_window)`

Estimates the accidental coincidence rate for two independent channels:

```text
R_acc = 2 * rate1 * rate2 * coincidence_window
```

---

### Signal utilities

Module:

```text
radlabpy.detectors.signals
```

#### `signal_to_noise(signal, noise)`

Computes:

```text
SNR = signal / noise
```

---

## `radlabpy.hep`

The `hep` subpackage contains basic high-energy physics kinematics utilities.

Module:

```text
radlabpy.hep.kinematics
```

Available functions:

```python
pt(px, py)
momentum(px, py, pz)
energy(px, py, pz, mass)
phi(px, py)
eta(px, py, pz)
invariant_mass(E, px, py, pz)
delta_phi(phi1, phi2)
delta_r(eta1, phi1, eta2, phi2)
```

The module uses natural units:

```text
c = 1
```

---

### `pt(px, py)`

Computes transverse momentum:

```text
pT = sqrt(px^2 + py^2)
```

---

### `momentum(px, py, pz)`

Computes the magnitude of the three-momentum:

```text
p = sqrt(px^2 + py^2 + pz^2)
```

---

### `energy(px, py, pz, mass)`

Computes relativistic energy:

```text
E = sqrt(px^2 + py^2 + pz^2 + m^2)
```

---

### `phi(px, py)`

Computes the azimuthal angle:

```text
phi = arctan2(py, px)
```

---

### `eta(px, py, pz)`

Computes pseudorapidity:

```text
eta = 0.5 * ln((p + pz) / (p - pz))
```

---

### `invariant_mass(E, px, py, pz)`

Computes invariant mass:

```text
m^2 = E^2 - px^2 - py^2 - pz^2
```

---

### `delta_phi(phi1, phi2)`

Computes angular separation in azimuth, accounting for periodicity.

---

### `delta_r(eta1, phi1, eta2, phi2)`

Computes angular separation:

```text
Delta R = sqrt((eta1 - eta2)^2 + Delta phi^2)
```

---

## `radlabpy.io`

The `io` module provides CSV input/output utilities.

Available functions:

```python
read_csv_data(path)
read_spectrum_csv(path, channel_col="channel", counts_col="counts")
read_counting_csv(path, counts_col="counts")
read_event_table(path)
write_summary_csv(summary, path)
```

The I/O module is intentionally limited to reading, validating, and writing data. It does not perform physics calculations.

---

## `radlabpy.plotting`

The `plotting` module provides Matplotlib-based scientific plotting utilities.

Available functions:

```python
plot_counts_time(time, counts, ax=None)
plot_spectrum(channels, counts, ax=None)
plot_gaussian_fit(x, y, fit_result, ax=None)
plot_calibration(channels, energies, calibration, ax=None)
plot_calibration_residuals(channels, residuals, ax=None)
plot_invariant_mass(masses, bins=50, ax=None)
```

Design conventions:

```text
all plotting functions return fig, ax
functions accept an existing axis through ax
functions do not call plt.show()
functions do not save figures automatically
plotting is separated from physical calculations
```

---

## `radlabpy.cli`

The command-line interface is available through:

```bash
radlab
```

Available commands:

```bash
radlab --help
radlab --version
radlab geiger data/geiger_sample.csv
radlab spectrum data/spectrum_sample.csv
radlab spectrum data/spectrum_sample.csv --fit-gaussian
radlab calibration data/calibration_sample.csv
radlab hep data/hep_events_sample.csv
radlab detector data/detector_sample.csv
```

The CLI is intended for quick, reproducible analyses from the terminal. It does not replace the Python API.

---

## Notes

This API reference corresponds to `radlabpy` version `0.1.0`.

Machine Learning utilities are intentionally not included in this release. They are planned for a future version.
