"""
Basic detector analysis example using radlabpy.

This example reads detector-like measurements from data/detector_sample.csv
and calculates:

- detection efficiency;
- binomial efficiency uncertainty;
- event rate;
- Poisson rate uncertainty;
- coincidence rate;
- accidental coincidence rate;
- signal-to-noise ratio.

Run from the project root with:

    python examples/detector_analysis.py
"""

from __future__ import annotations

from pathlib import Path

from radlabpy.detectors import (
    accidental_coincidence_rate,
    coincidence_rate,
    detection_efficiency,
    efficiency_uncertainty,
    event_rate,
    rate_uncertainty,
    signal_to_noise,
)
from radlabpy.io import read_csv_data, write_summary_csv


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "detector_sample.csv"
    output_path = project_root / "data" / "detector_summary.csv"

    data = read_csv_data(data_path)

    summaries = []

    print("Basic detector analysis")
    print("=======================")
    print(f"Input file: {data_path}")

    for _, row in data.iterrows():
        efficiency = detection_efficiency(row["detected"], row["emitted"])
        sigma_efficiency = efficiency_uncertainty(row["detected"], row["emitted"])

        rate = event_rate(row["counts"], row["time"])
        sigma_rate = rate_uncertainty(row["counts"], row["time"])

        coincidence = coincidence_rate(row["coincidences"], row["time"])

        accidental = accidental_coincidence_rate(
            row["rate1"],
            row["rate2"],
            row["coincidence_window"],
        )

        snr = signal_to_noise(row["signal"], row["noise"])

        summary = {
            "measurement": int(row["measurement"]),
            "efficiency": efficiency,
            "efficiency_uncertainty": sigma_efficiency,
            "rate": rate,
            "rate_uncertainty": sigma_rate,
            "coincidence_rate": coincidence,
            "accidental_coincidence_rate": accidental,
            "signal_to_noise": snr,
        }

        summaries.append(summary)

        print()
        print(f"Measurement {int(row['measurement'])}")
        print("----------------")
        print(f"Detection efficiency:       {efficiency:.4f}")
        print(f"Efficiency uncertainty:     {sigma_efficiency:.4f}")
        print(f"Event rate:                 {rate:.4f} counts/s")
        print(f"Rate uncertainty:           {sigma_rate:.4f} counts/s")
        print(f"Coincidence rate:           {coincidence:.4f} coincidences/s")
        print(f"Accidental coincidence rate:{accidental:.6e} Hz")
        print(f"Signal-to-noise ratio:      {snr:.4f}")

    written_path = write_summary_csv(summaries, output_path)

    print()
    print("Output")
    print("======")
    print(f"Summary written to: {written_path}")


if __name__ == "__main__":
    main()