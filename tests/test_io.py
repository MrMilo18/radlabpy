"""
Tests for radlabpy.io.
"""

from __future__ import annotations

import pandas as pd
import pytest

from radlabpy.io import (
    read_counting_csv,
    read_csv_data,
    read_event_table,
    read_spectrum_csv,
    write_summary_csv,
)


def test_read_csv_data_reads_temporary_csv(tmp_path):
    csv_path = tmp_path / "sample.csv"

    original = pd.DataFrame(
        {
            "time": [0.0, 1.0, 2.0],
            "counts": [20, 25, 23],
        }
    )
    original.to_csv(csv_path, index=False)

    data = read_csv_data(csv_path)

    assert isinstance(data, pd.DataFrame)
    assert list(data.columns) == ["time", "counts"]
    assert len(data) == 3
    assert data["counts"].tolist() == [20, 25, 23]


def test_read_csv_data_missing_file_raises_file_not_found(tmp_path):
    missing_path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        read_csv_data(missing_path)


def test_read_spectrum_csv_validates_channel_and_counts_columns(tmp_path):
    csv_path = tmp_path / "spectrum.csv"

    pd.DataFrame(
        {
            "channel": [0, 1, 2],
            "counts": [10, 50, 20],
        }
    ).to_csv(csv_path, index=False)

    data = read_spectrum_csv(csv_path)

    assert isinstance(data, pd.DataFrame)
    assert "channel" in data.columns
    assert "counts" in data.columns


def test_read_spectrum_csv_missing_required_column_raises_value_error(tmp_path):
    csv_path = tmp_path / "bad_spectrum.csv"

    pd.DataFrame(
        {
            "channel": [0, 1, 2],
            "intensity": [10, 50, 20],
        }
    ).to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match="Missing required column"):
        read_spectrum_csv(csv_path)


def test_read_counting_csv_validates_counts_column(tmp_path):
    csv_path = tmp_path / "counts.csv"

    pd.DataFrame(
        {
            "time": [0.0, 1.0, 2.0],
            "counts": [22, 25, 24],
        }
    ).to_csv(csv_path, index=False)

    data = read_counting_csv(csv_path)

    assert isinstance(data, pd.DataFrame)
    assert "counts" in data.columns


def test_read_counting_csv_missing_counts_column_raises_value_error(tmp_path):
    csv_path = tmp_path / "bad_counts.csv"

    pd.DataFrame(
        {
            "time": [0.0, 1.0, 2.0],
            "cpm": [22, 25, 24],
        }
    ).to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match="Missing required column"):
        read_counting_csv(csv_path)


def test_read_event_table_returns_dataframe(tmp_path):
    csv_path = tmp_path / "events.csv"

    pd.DataFrame(
        {
            "E": [50.0, 45.0],
            "px": [30.0, -20.0],
            "py": [10.0, -5.0],
            "pz": [40.0, -30.0],
        }
    ).to_csv(csv_path, index=False)

    data = read_event_table(csv_path)

    assert isinstance(data, pd.DataFrame)
    assert list(data.columns) == ["E", "px", "py", "pz"]


def test_write_summary_csv_writes_output_file(tmp_path):
    output_path = tmp_path / "summary.csv"

    summary = {
        "mean_counts": 25.0,
        "std_counts": 2.0,
        "n_measurements": 10,
    }

    written_path = write_summary_csv(summary, output_path)

    assert written_path == output_path
    assert output_path.exists()

    data = pd.read_csv(output_path)

    assert list(data.columns) == ["mean_counts", "std_counts", "n_measurements"]
    assert data.loc[0, "mean_counts"] == 25.0
    assert data.loc[0, "std_counts"] == 2.0
    assert data.loc[0, "n_measurements"] == 10