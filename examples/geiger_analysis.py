"""
Example: basic Geiger counter analysis with radlabpy.

This script demonstrates how to:

1. Read counting data from data/geiger_sample.csv.
2. Compute a counting summary.
3. Convert CPM and CPS.
4. Plot counts as a function of time.

Run from the project root with:

    python examples/geiger_analysis.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from radlabpy.io import read_counting_csv
from radlabpy.plotting import plot_counts_time
from radlabpy.radiation import (
    counting_summary,
    count_rate,
    cps_to_cpm,
    cpm_to_cps,
    poisson_uncertainty,
)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "geiger_sample.csv"

    data = read_counting_csv(data_path)

    times = data["time"]
    counts = data["counts"]

    summary = counting_summary(counts)

    print("Geiger counter analysis")
    print("=======================")
    print(f"Input file: {data_path}")
    print(f"Number of measurements: {summary['n_measurements']}")
    print(f"Total counts: {summary['total_counts']:.2f}")
    print(f"Mean counts: {summary['mean_counts']:.2f}")
    print(f"Std counts: {summary['std_counts']:.2f}")
    print(f"Poisson uncertainty of mean counts: {summary['poisson_uncertainty_mean']:.2f}")

    mean_cpm = summary["mean_counts"]
    mean_cps = cpm_to_cps(mean_cpm)

    print()
    print("Rate conversion")
    print("===============")
    print(f"Mean CPM: {mean_cpm:.2f}")
    print(f"Mean CPS: {mean_cps:.4f}")
    print(f"Back to CPM: {cps_to_cpm(mean_cps):.2f}")

    total_time = times.iloc[-1] - times.iloc[0] + 60.0
    total_counts = summary["total_counts"]
    rate = count_rate(total_counts, total_time)
    uncertainty = poisson_uncertainty(total_counts)

    print()
    print("Full measurement")
    print("================")
    print(f"Total counts: {total_counts:.2f}")
    print(f"Total time: {total_time:.1f} s")
    print(f"Average rate: {rate:.4f} cps")
    print(f"Poisson uncertainty: {uncertainty:.2f} counts")

    fig, ax = plot_counts_time(
        times,
        counts,
        title="Geiger sample data",
        xlabel="Time [s]",
        ylabel="Counts per 60 s",
    )

    plt.show()


if __name__ == "__main__":
    main()