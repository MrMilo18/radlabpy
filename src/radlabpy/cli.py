"""
Command line interface for radlabpy.

This module provides a small but functional CLI for quick analyses from
the terminal. The CLI does not implement new scientific calculations;
its calls the public function already available in radlabpy.
"""

from __future__ import annotations

import argparse
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import numpy as np

from radlabpy.io import (
    read_counting_csv,
    read_csv_data,
    read_event_table,
    read_spectrum_csv,
)
from radlabpy.radiation.counting import counting_summary
from radlabpy.radiation.spectra import find_peak_channel, total_counts
from radlabpy.radiation.fitting import fit_gaussian_peak, fwhm_from_sigma
from radlabpy.radiation.calibration import linear_calibration, calibration_residuals
from radlabpy.hep.kinematics import invariant_mass
from radlabpy.detectors.efficiency import detection_efficiency, efficiency_uncertainty
from radlabpy.detectors.rates import event_rate, rate_uncertainty
from radlabpy.detectors.signals import signal_to_noise

def _get_version() -> str:
    """Return the installed package version."""
    try:
        return version("radlabpy")
    except PackageNotFoundError:
        return "unknown"
    

def _check_file_exists(path: str | Path) -> Path:
    """Validate that an input file exists."""
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")
    
    if not file_path.is_file():
        raise ValueError(f"Input path is not a file: {file_path}")
    
    return file_path


def _print_header(title: str) -> None:
    """Print a simple CLI section header."""
    print(f"\n{title}")
    print("-" * len(title))


def _format_float(value: float) -> str:
    """Format numerical output consistently."""
    return f"{float(value):.6}"

def _get_summary_value(summary: dict, *possible_keys: str):
    """Read a value from a summary dictionary using possible key names."""
    for key in possible_keys:
        if key in summary:
            return summary[key]
    return None

def run_geiger(args: argparse.Namespace) -> int:
    """Run Geiger counting analysis."""
    path = _check_file_exists(args.file)

    data = read_counting_csv(path, counts_col=args.counts_col)
    counts = data[args.counts_col].to_numpy(dtype = float)

    summary = counting_summary(counts)

    n = _get_summary_value(summary, "n", "size", "counts", "num_points")
    mean = _get_summary_value(summary, "mean", "average")
    std = _get_summary_value(summary, "std", "standard_deviation", "std_dev")
    minimum = _get_summary_value(summary, "min", "minimum")
    maximum = _get_summary_value(summary, "max", "maximum")

    _print_header("Geiger counting summary")
    print(f"File: {path}")
    print(f"Counts column: {args.counts_col}")

    if n is not None:
        print(f"N: {n}")
    else:
        print(f"N: {counts.size}")

    if mean is not None:
        print(f"Mean: {_format_float(mean)}")
    else:
        print(f"Mean: {_format_float(np.mean(counts))}")

    if std is not None:
        print(f"Standard deviation: {_format_float(std)}")
    else:
        print(f"Standard deviation: {_format_float(np.std(counts, ddof=1))}")

    if minimum is not None:
        print(f"Minimum: {_format_float(minimum)}")
    else:
        print(f"Minimum: {_format_float(np.min(counts))}")

    if maximum is not None:
        print(f"Maximum: {_format_float(maximum)}")
    else:
        print(f"Maximum: {_format_float(np.max(counts))}")

    return 0


def run_spectrum(args: argparse.Namespace) -> int:
    """Run spectrum analysis."""
    path = _check_file_exists(args.file)

    spectrum = read_spectrum_csv(
        path,
        channel_col=args.channel_col,
        counts_col=args.counts_col,
    )

    channels = spectrum[args.channel_col].to_numpy(dtype=float)
    counts = spectrum[args.counts_col].to_numpy(dtype=float)

    peak_channel = find_peak_channel(channels, counts)
    counts_total = total_counts(counts)

    _print_header("Spectrum summary")
    print(f"File: {path}")
    print(f"Channel column: {args.channel_col}")
    print(f"Counts column: {args.counts_col}")
    print(f"Total counts: {_format_float(counts_total)}")
    print(f"Peak channel: {_format_float(peak_channel)}")

    if args.fit_gaussian:
        fit = fit_gaussian_peak(channels, counts)
        fwhm = fwhm_from_sigma(fit["sigma"])

        print("\nGaussian fit")
        print(f"Amplitude: {_format_float(fit['amplitude'])}")
        print(f"Mean: {_format_float(fit['mean'])}")
        print(f"Sigma: {_format_float(fit['sigma'])}")
        print(f"FWHM: {_format_float(fwhm)}")

        if "background" in fit:
            print(f"Background: {_format_float(fit['background'])}")

    return 0


def run_calibration(args: argparse.Namespace) -> int:
    """Run linear energy calibration."""
    path = _check_file_exists(args.file)

    data = read_csv_data(path)

    if args.channel_col not in data.columns:
        raise ValueError(f"Missing channel column: {args.channel_col}")

    if args.energy_col not in data.columns:
        raise ValueError(f"Missing energy column: {args.energy_col}")

    channels = data[args.channel_col].to_numpy(dtype=float)
    energies = data[args.energy_col].to_numpy(dtype=float)

    calibration = linear_calibration(channels, energies)
    residuals = calibration_residuals(channels, energies, calibration)

    slope = calibration["slope"]
    intercept = calibration["intercept"]
    r_squared = calibration.get("r_squared", None)

    _print_header("Energy calibration")
    print(f"File: {path}")
    print(f"Relation: E = slope * channel + intercept")
    print(f"Slope: {_format_float(slope)}")
    print(f"Intercept: {_format_float(intercept)}")

    if r_squared is not None:
        print(f"R squared: {_format_float(r_squared)}")

    print(f"Residual mean: {_format_float(np.mean(residuals))}")
    print(f"Residual std: {_format_float(np.std(residuals, ddof=1))}")

    return 0


def run_hep(args: argparse.Namespace) -> int:
    """Run a minimal HEP event analysis."""
    path = _check_file_exists(args.file)

    events = read_event_table(path)
    required_columns = ["E", "px", "py", "pz"]

    missing = [col for col in required_columns if col not in events.columns]
    if missing:
        raise ValueError(
            "HEP analysis requires columns E, px, py, pz. "
            f"Missing columns: {', '.join(missing)}"
        )

    E = events["E"].to_numpy(dtype=float)
    px = events["px"].to_numpy(dtype=float)
    py = events["py"].to_numpy(dtype=float)
    pz = events["pz"].to_numpy(dtype=float)

    masses = invariant_mass(E, px, py, pz)

    _print_header("HEP invariant mass summary")
    print(f"File: {path}")
    print(f"Number of events: {masses.size}")
    print(f"Mean mass: {_format_float(np.mean(masses))}")
    print(f"Standard deviation: {_format_float(np.std(masses, ddof=1))}")
    print(f"Minimum mass: {_format_float(np.min(masses))}")
    print(f"Maximum mass: {_format_float(np.max(masses))}")

    return 0


def run_detector(args: argparse.Namespace) -> int:
    """Run a minimal detector analysis based on available columns."""
    path = _check_file_exists(args.file)

    data = read_csv_data(path)

    _print_header("Detector summary")
    print(f"File: {path}")
    print(f"Columns: {', '.join(data.columns)}")

    did_something = False

    if {"detected", "emitted"}.issubset(data.columns):
        detected = data["detected"].to_numpy(dtype=float)
        emitted = data["emitted"].to_numpy(dtype=float)

        efficiency = detection_efficiency(detected, emitted)
        uncertainty = efficiency_uncertainty(detected, emitted)

        print("\nEfficiency")
        print(f"Mean efficiency: {_format_float(np.mean(efficiency))}")
        print(f"Mean uncertainty: {_format_float(np.mean(uncertainty))}")
        did_something = True

    if {"counts", "time"}.issubset(data.columns):
        counts = data["counts"].to_numpy(dtype=float)
        time = data["time"].to_numpy(dtype=float)

        rates = event_rate(counts, time)
        uncertainties = rate_uncertainty(counts, time)

        print("\nEvent rate")
        print(f"Mean rate: {_format_float(np.mean(rates))}")
        print(f"Mean rate uncertainty: {_format_float(np.mean(uncertainties))}")
        did_something = True

    if {"signal", "noise"}.issubset(data.columns):
        signal = data["signal"].to_numpy(dtype=float)
        noise = data["noise"].to_numpy(dtype=float)

        snr = signal_to_noise(signal, noise)

        print("\nSignal-to-noise ratio")
        print(f"Mean SNR: {_format_float(np.mean(snr))}")
        did_something = True

    if not did_something:
        raise ValueError(
            "No compatible detector columns found. "
            "Expected one of: detected/emitted, counts/time, signal/noise."
        )

    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the radlab command."""
    parser = argparse.ArgumentParser(
        prog="radlab",
        description=(
            "Command line interface for radlabpy: radiation, detector "
            "and HEP analysis utilities."
        ),
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"radlabpy {_get_version()}",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    geiger_parser = subparsers.add_parser(
        "geiger",
        help="Analyze Geiger counting data from a CSV file.",
    )
    geiger_parser.add_argument("file", help="Input CSV file.")
    geiger_parser.add_argument(
        "--counts-col",
        default="counts",
        help="Name of the counts column.",
    )
    geiger_parser.set_defaults(func=run_geiger)

    spectrum_parser = subparsers.add_parser(
        "spectrum",
        help="Analyze a radiation spectrum from a CSV file.",
    )
    spectrum_parser.add_argument("file", help="Input CSV file.")
    spectrum_parser.add_argument(
        "--channel-col",
        default="channel",
        help="Name of the channel column.",
    )
    spectrum_parser.add_argument(
        "--counts-col",
        default="counts",
        help="Name of the counts column.",
    )
    spectrum_parser.add_argument(
        "--fit-gaussian",
        action="store_true",
        help="Fit a Gaussian peak to the spectrum.",
    )
    spectrum_parser.set_defaults(func=run_spectrum)

    calibration_parser = subparsers.add_parser(
        "calibration",
        help="Perform a linear channel-energy calibration.",
    )
    calibration_parser.add_argument("file", help="Input CSV file.")
    calibration_parser.add_argument(
        "--channel-col",
        default="channel",
        help="Name of the channel column.",
    )
    calibration_parser.add_argument(
        "--energy-col",
        default="energy",
        help="Name of the energy column.",
    )
    calibration_parser.set_defaults(func=run_calibration)

    hep_parser = subparsers.add_parser(
        "hep",
        help="Analyze HEP event data and compute invariant masses.",
    )
    hep_parser.add_argument("file", help="Input CSV file.")
    hep_parser.set_defaults(func=run_hep)

    detector_parser = subparsers.add_parser(
        "detector",
        help="Analyze simple detector data.",
    )
    detector_parser.add_argument("file", help="Input CSV file.")
    detector_parser.set_defaults(func=run_detector)

    return parser


def main(argv: list[str] | None = None) -> int:
    """
    Run the radlab command line interface.

    Parameters
    ----------
    argv : list of str, optional
        Command line arguments. If None, arguments are read from sys.argv.

    Returns
    -------
    int
        Exit code. Returns 0 when the command succeeds and non-zero when
        a controlled error occurs.
    """
    parser = build_parser()

    try:
        args = parser.parse_args(argv)
        return args.func(args)

    except SystemExit as exc:
        return int(exc.code)

    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())