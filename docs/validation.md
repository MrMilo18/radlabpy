# Scientific Validation

This document summarizes the scientific and numerical validation strategy used in `radlabpy` version `0.1.0`.

In scientific software, it is not enough for code to run without errors. The implemented functions must also produce results consistent with known physical, mathematical, or statistical expectations.

`radlabpy` uses unit tests, controlled examples, analytical formulas, and physical constraints to validate its main functionality.

---

## Validation philosophy

The validation strategy of `radlabpy` is based on the following principles:

* test simple cases with known analytical results;
* check physical constraints such as non-negative counts, positive times, and non-negative masses;
* verify consistency between related formulas;
* separate numerical calculation from plotting and input/output;
* use reproducible sample data;
* run automated tests with `pytest`;
* document the physical conventions used by the package.

---

## Counting statistics

### Poisson uncertainty

For counting experiments, `radlabpy` uses the standard Poisson approximation:

```text
sigma_N = sqrt(N)
```

Validation case:

```text
N = 100
sigma_N = sqrt(100) = 10
```

Expected result:

```text
poisson_uncertainty(100) = 10
```

This validates that the implemented uncertainty follows the expected square-root scaling for Poisson-distributed counts.

---

### Count validation

Radiation counts must be non-negative.

Invalid cases:

```text
counts < 0
```

Expected behavior:

```text
raise ValueError
```

This prevents physically meaningless negative counting measurements.

---

### Counting summary

For a list of count measurements, the summary should include:

```text
number of measurements
total counts
mean counts
standard deviation
minimum count
maximum count
Poisson uncertainty of the mean count
```

Validation strategy:

* compare the mean with `numpy.mean`;
* compare the standard deviation with `numpy.std(..., ddof=1)`;
* verify that empty inputs raise an error;
* verify that negative counts raise an error.

---

## Count rates

The count rate is defined as:

```text
rate = counts / time
```

Validation case:

```text
counts = 1200
time = 60 s
rate = 1200 / 60 = 20 counts/s
```

Expected result:

```text
count_rate(1200, 60) = 20
```

The measurement time must be strictly positive.

Invalid cases:

```text
time <= 0
```

Expected behavior:

```text
raise ValueError
```

---

## CPS and CPM conversion

The conversion between counts per second and counts per minute is:

```text
CPM = 60 * CPS
CPS = CPM / 60
```

Validation case:

```text
CPS = 2
CPM = 120
```

Expected results:

```text
cps_to_cpm(2) = 120
cpm_to_cps(120) = 2
```

These conversions also provide an internal consistency check:

```text
cpm_to_cps(cps_to_cpm(x)) = x
```

---

## Spectrum analysis

### Total counts

The total number of counts in a spectrum is:

```text
N_total = sum(counts)
```

Validation case:

```text
counts = [1, 2, 3, 4]
N_total = 10
```

Expected result:

```text
total_counts([1, 2, 3, 4]) = 10
```

Invalid cases:

```text
empty spectrum
negative counts
non-finite values
```

Expected behavior:

```text
raise ValueError
```

---

### Spectrum normalization

A normalized spectrum should satisfy:

```text
sum(normalized_counts) = 1
```

Validation strategy:

* normalize a simple spectrum;
* verify that the sum is numerically close to 1;
* reject spectra with zero total counts.

Invalid case:

```text
counts = [0, 0, 0]
```

Expected behavior:

```text
raise ValueError
```

---

### Peak channel

The peak channel is the channel corresponding to the maximum count value.

Validation case:

```text
channels = [0, 1, 2, 3]
counts = [4, 7, 12, 5]
```

Expected result:

```text
find_peak_channel(channels, counts) = 2
```

The function also validates that channels and counts have compatible shapes.

---

## Gaussian peak analysis

### Gaussian model

The Gaussian model used by `radlabpy` is:

```text
y = amplitude * exp(-(x - mean)^2 / (2 sigma^2)) + background
```

Validation strategy:

* evaluate the function at the mean;
* verify that the value at the mean equals `amplitude + background`;
* reject non-positive sigma values.

Validation case:

```text
x = mean
y = amplitude + background
```

---

### FWHM

For a Gaussian peak, the full width at half maximum is:

```text
FWHM = 2 * sqrt(2 * ln(2)) * sigma
```

Validation case:

```text
sigma = 1
FWHM ≈ 2.354820045
```

Expected result:

```text
fwhm_from_sigma(1) ≈ 2.3548
```

---

### Energy resolution

The relative energy resolution is:

```text
R = FWHM / E
```

Validation case:

```text
FWHM = 5
E = 100
R = 0.05
```

Expected result:

```text
energy_resolution(5, 100) = 0.05
```

Invalid cases:

```text
FWHM < 0
E <= 0
```

Expected behavior:

```text
raise ValueError
```

---

### Gaussian peak area

The estimated area under a Gaussian peak without background is:

```text
area = amplitude * sigma * sqrt(2*pi)
```

Validation strategy:

* use simple amplitude and sigma values;
* compare with the analytical expression;
* reject negative amplitudes and non-positive sigma values.

---

### Gaussian fitting

The Gaussian fitting routine is validated using synthetic spectra generated from known parameters.

Validation strategy:

1. Generate a synthetic Gaussian peak.
2. Fit the peak using `fit_gaussian_peak`.
3. Verify that the fitted mean is close to the known peak center.
4. Verify that the fitted sigma is positive.
5. Verify that the fitted amplitude is positive.

This validates that the fitting routine can recover reasonable parameters from controlled data.

---

## Energy calibration

### Linear calibration

The calibration convention used in `radlabpy` is:

```text
E = slope * channel + intercept
```

Validation case:

```text
channels = [100, 200, 300]
energies = [1.0, 2.0, 3.0]
```

Expected calibration:

```text
slope = 0.01
intercept = 0
```

Validation strategy:

* fit synthetic data with a known linear relation;
* verify that the recovered slope and intercept are correct within numerical tolerance;
* verify that `R^2` is close to 1 for perfectly linear data.

---

### Channel-energy conversion

The two conversion functions should be internally consistent:

```text
energy = channel_to_energy(channel, calibration)
channel = energy_to_channel(energy, calibration)
```

Validation condition:

```text
energy_to_channel(channel_to_energy(channel, calibration), calibration) ≈ channel
```

---

### Calibration residuals

Residuals are defined as:

```text
residual = observed_energy - calibrated_energy
```

For perfectly linear synthetic data, residuals should be close to zero.

Validation case:

```text
observed_energy = calibrated_energy
residual = 0
```

---

## Detector analysis

### Detection efficiency

Detection efficiency is defined as:

```text
efficiency = detected / emitted
```

Validation case:

```text
detected = 850
emitted = 1000
efficiency = 0.85
```

Expected result:

```text
detection_efficiency(850, 1000) = 0.85
```

Physical constraints:

```text
detected >= 0
emitted > 0
detected <= emitted
```

Invalid cases should raise `ValueError`.

---

### Efficiency uncertainty

The approximate binomial uncertainty is:

```text
sigma_eff = sqrt(efficiency * (1 - efficiency) / emitted)
```

Validation strategy:

* compute efficiency;
* compute the uncertainty using the analytical formula;
* compare with the function output.

This uncertainty is statistical only and does not include systematic effects.

---

### Event rate

The event rate is:

```text
rate = counts / time
```

Validation case:

```text
counts = 1200
time = 60
rate = 20
```

Expected result:

```text
event_rate(1200, 60) = 20
```

---

### Rate uncertainty

For Poisson counting statistics:

```text
sigma_rate = sqrt(counts) / time
```

Validation case:

```text
counts = 100
time = 10
sigma_rate = sqrt(100) / 10 = 1
```

Expected result:

```text
rate_uncertainty(100, 10) = 1
```

---

### Coincidence rate

The coincidence rate is:

```text
coincidence_rate = coincidences / time
```

Validation case:

```text
coincidences = 180
time = 60
coincidence_rate = 3
```

Expected result:

```text
coincidence_rate(180, 60) = 3
```

---

### Accidental coincidence rate

For two independent detector channels and a symmetric coincidence window:

```text
R_acc = 2 * rate1 * rate2 * coincidence_window
```

Validation case:

```text
rate1 = 25 Hz
rate2 = 30 Hz
coincidence_window = 100e-9 s
```

Expected result:

```text
R_acc = 2 * 25 * 30 * 100e-9
R_acc = 1.5e-4 Hz
```

---

### Signal-to-noise ratio

The signal-to-noise ratio is:

```text
SNR = signal / noise
```

Validation case:

```text
signal = 50
noise = 5
SNR = 10
```

Expected result:

```text
signal_to_noise(50, 5) = 10
```

The noise must be greater than zero.

Invalid cases:

```text
noise <= 0
```

Expected behavior:

```text
raise ValueError
```

---

## High-energy physics kinematics

The HEP module uses natural units:

```text
c = 1
```

All energies, momenta and masses must be given in compatible units, for example GeV.

---

### Transverse momentum

The transverse momentum is:

```text
pT = sqrt(px^2 + py^2)
```

Validation case:

```text
px = 3
py = 4
pT = 5
```

Expected result:

```text
pt(3, 4) = 5
```

---

### Momentum magnitude

The three-momentum magnitude is:

```text
p = sqrt(px^2 + py^2 + pz^2)
```

Validation case:

```text
px = 3
py = 4
pz = 12
p = 13
```

Expected result:

```text
momentum(3, 4, 12) = 13
```

---

### Relativistic energy

The relativistic energy is:

```text
E = sqrt(px^2 + py^2 + pz^2 + m^2)
```

Validation case:

```text
px = 3
py = 4
pz = 0
m = 2
E = sqrt(3^2 + 4^2 + 0^2 + 2^2)
E = sqrt(29)
```

---

### Invariant mass

The invariant mass is:

```text
m^2 = E^2 - px^2 - py^2 - pz^2
```

Validation case for a particle at rest:

```text
px = 0
py = 0
pz = 0
E = m
```

Expected result:

```text
invariant_mass(E, 0, 0, 0) = E
```

The function rejects four-momenta with negative mass squared beyond numerical tolerance.

---

### Azimuthal angle

The azimuthal angle is:

```text
phi = arctan2(py, px)
```

Validation cases:

```text
phi(1, 0) = 0
phi(0, 1) = pi/2
```

---

### Pseudorapidity

The pseudorapidity is:

```text
eta = 0.5 * ln((p + pz) / (p - pz))
```

Validation strategy:

* verify finite results for valid nonzero momentum;
* reject zero-momentum inputs, where pseudorapidity is undefined.

---

### Delta phi

The angular difference in azimuth must account for periodicity.

Validation strategy:

* verify that the result lies in the interval `[-pi, pi]`;
* test angles near the `-pi` and `pi` boundary.

---

### Delta R

The angular separation is:

```text
Delta R = sqrt((eta1 - eta2)^2 + Delta phi^2)
```

Validation case:

```text
eta1 = eta2
phi1 = phi2
Delta R = 0
```

Expected result:

```text
delta_r(eta, phi, eta, phi) = 0
```

---

## Input/output validation

The I/O module validates that input files exist and that required columns are present.

Examples of required columns:

```text
counting data: counts
spectrum data: channel, counts
HEP data: E, px, py, pz
calibration data: channel, energy
```

Validation strategy:

* missing files raise `FileNotFoundError`;
* missing required columns raise `ValueError`;
* data reading is separated from physical calculations.

---

## Plotting validation

Plotting functions are validated mainly by checking that they:

* return a Matplotlib `fig, ax` pair;
* do not call `plt.show()` internally;
* do not save files automatically;
* accept an existing axis through `ax`;
* can be used in automated tests without requiring interactive display.

This keeps visualization separate from scientific calculation.

---

## Command-line interface validation

The CLI is tested using `pytest`.

Validation strategy:

* verify that `radlab --help` runs correctly;
* verify that `radlab --version` runs correctly;
* verify that each subcommand can process its corresponding sample dataset;
* verify that controlled invalid inputs produce controlled errors.

Main commands validated:

```bash
radlab geiger data/geiger_sample.csv
radlab spectrum data/spectrum_sample.csv
radlab spectrum data/spectrum_sample.csv --fit-gaussian
radlab calibration data/calibration_sample.csv
radlab hep data/hep_events_sample.csv
radlab detector data/detector_sample.csv
```

---

## Test suite

Run the complete test suite with:

```bash
pytest
```

The current tests cover:

```text
radiation counting
spectrum utilities
Gaussian fitting
energy calibration
detector utilities
HEP kinematics
CSV input/output
scientific plotting
command-line interface
```

---

## Limitations of version 0.1.0

The current validation is appropriate for an initial academic release, but it is not a replacement for full experimental validation.

Current limitations include:

* no full systematic uncertainty treatment;
* no ROOT file support;
* no detector simulation;
* no advanced likelihood fitting;
* no complete HEP event reconstruction;
* no Machine Learning module in this release;
* only small sample datasets are included.

These limitations are intentional. Version `0.1.0` focuses on a clean, tested, and extensible scientific core.

---

## Future validation improvements

Possible improvements for future versions include:

* benchmark datasets;
* comparison against external tools;
* more realistic detector examples;
* larger synthetic spectra;
* uncertainty propagation tests;
* validation notebooks;
* continuous integration with automated testing;
* regression tests for future releases.

---

## Summary

The validation of `radlabpy` version `0.1.0` is based on simple but physically meaningful checks:

* Poisson counting uncertainty scales as `sqrt(N)`;
* count rates follow `counts / time`;
* Gaussian FWHM follows the analytical relation with `sigma`;
* energy calibration recovers known linear relations;
* detector efficiency remains between 0 and 1;
* HEP invariant mass follows the relativistic four-momentum convention;
* plotting remains separated from calculation;
* command-line workflows are tested with sample data.

This provides a reliable foundation for an academic scientific Python package and prepares the project for future extensions.
