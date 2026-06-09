"""
Example: basic Geiger counter analysis with radlabpy.

This script demonstrates the use of the radiation counting utilities.
"""

from radlabpy.radiation import (
    poisson_uncertainty,
    counting_summary,
    count_rate,
    cps_to_cpm,
    cpm_to_cps,
)


def main():
    # Example measurements in counts per minute.
    cpm_measurements = [22, 25, 24, 27, 23, 26, 25, 24, 28, 23]

    summary = counting_summary(cpm_measurements)

    print("Geiger counter analysis")
    print("=======================")
    print(f"Number of measurements: {summary['n_measurements']}")
    print(f"Total counts: {summary['total_counts']:.2f}")
    print(f"Mean CPM: {summary['mean_counts']:.2f}")
    print(f"Std CPM: {summary['std_counts']:.2f}")
    print(f"Poisson uncertainty of mean CPM: {summary['poisson_uncertainty_mean']:.2f}")

    mean_cpm = summary["mean_counts"]
    mean_cps = cpm_to_cps(mean_cpm)

    print()
    print("Rate conversion")
    print("===============")
    print(f"Mean CPM: {mean_cpm:.2f}")
    print(f"Mean CPS: {mean_cps:.4f}")
    print(f"Back to CPM: {cps_to_cpm(mean_cps):.2f}")

    counts = 120
    time = 60
    rate = count_rate(counts, time)
    uncertainty = poisson_uncertainty(counts)

    print()
    print("Single measurement")
    print("==================")
    print(f"Counts: {counts}")
    print(f"Time: {time} s")
    print(f"Rate: {rate:.2f} cps")
    print(f"Poisson uncertainty: {uncertainty:.2f} counts")


if __name__ == "__main__":
    main()