"""
Input/output utilities for radlabpy.

This module contains functions for reading and writing simple tabular
data files used in radiation, detector and HEP examples.

The functions in this module are intentionally limited to I/O tasks:
they read data, validate file existence, validate required columns, and
write tabular summaries. They do not perform physics calculations.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def _as_path(path: str | Path) -> Path:
    """
    Convert a string or Path-like object to a pathlib.Path.

    Parameters
    ----------
    path : str or pathlib.Path
        Input file or output file path.

    Returns
    -------
    pathlib.Path
        Normalized path object.
    """
    return Path(path)


def _check_file_exists(path: str | Path) -> Path:
    """
    Check that an input file exists.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the input file.

    Returns
    -------
    pathlib.Path
        Validated path.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    """
    file_path = _as_path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.is_file():
        raise FileNotFoundError(f"Path is not a file: {file_path}")

    return file_path


def _validate_columns(data: pd.DataFrame, required_columns: list[str]) -> None:
    """
    Validate that a DataFrame contains required columns.

    Parameters
    ----------
    data : pandas.DataFrame
        Input table.
    required_columns : list of str
        Column names that must be present.

    Raises
    ------
    ValueError
        If one or more required columns are missing.
    """
    missing_columns = [column for column in required_columns if column not in data.columns]

    if missing_columns:
        raise ValueError(
            "Missing required column(s): "
            + ", ".join(missing_columns)
            + f". Available columns: {list(data.columns)}"
        )


def read_csv_data(path: str | Path) -> pd.DataFrame:
    """
    Read a generic CSV file as a pandas DataFrame.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the CSV file.

    Returns
    -------
    pandas.DataFrame
        Data read from the CSV file.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    """
    file_path = _check_file_exists(path)
    return pd.read_csv(file_path)


def read_spectrum_csv(
    path: str | Path,
    channel_col: str = "channel",
    counts_col: str = "counts",
) -> pd.DataFrame:
    """
    Read a spectrum CSV file and validate channel and counts columns.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the CSV file.
    channel_col : str, optional
        Name of the channel column. Default is ``"channel"``.
    counts_col : str, optional
        Name of the counts column. Default is ``"counts"``.

    Returns
    -------
    pandas.DataFrame
        Spectrum table.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If required columns are missing.
    """
    data = read_csv_data(path)
    _validate_columns(data, [channel_col, counts_col])
    return data


def read_counting_csv(
    path: str | Path,
    counts_col: str = "counts",
) -> pd.DataFrame:
    """
    Read a counting CSV file and validate the counts column.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the CSV file.
    counts_col : str, optional
        Name of the counts column. Default is ``"counts"``.

    Returns
    -------
    pandas.DataFrame
        Counting data table.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the counts column is missing.
    """
    data = read_csv_data(path)
    _validate_columns(data, [counts_col])
    return data


def read_event_table(path: str | Path) -> pd.DataFrame:
    """
    Read a generic event table from a CSV file.

    This function is intended for simple tabular event data, for example
    HEP-like tables with columns such as ``E``, ``px``, ``py`` and ``pz``.
    It only reads the file and returns a DataFrame. Physics-specific
    validation should be done elsewhere.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the CSV file.

    Returns
    -------
    pandas.DataFrame
        Event table.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    """
    return read_csv_data(path)


def write_summary_csv(summary: dict[str, Any] | list[dict[str, Any]] | pd.DataFrame, path: str | Path) -> Path:
    """
    Write a summary object to a CSV file.

    Parameters
    ----------
    summary : dict, list of dict, or pandas.DataFrame
        Summary data to write. A dictionary is written as a single-row
        CSV file.
    path : str or pathlib.Path
        Output CSV file path.

    Returns
    -------
    pathlib.Path
        Path to the written CSV file.

    Raises
    ------
    ValueError
        If the summary format is not supported.
    """
    output_path = _as_path(path)

    if isinstance(summary, pd.DataFrame):
        data = summary
    elif isinstance(summary, dict):
        data = pd.DataFrame([summary])
    elif isinstance(summary, list):
        data = pd.DataFrame(summary)
    else:
        raise ValueError(
            "summary must be a dictionary, a list of dictionaries, or a pandas DataFrame."
        )

    if output_path.parent != Path("."):
        output_path.parent.mkdir(parents=True, exist_ok=True)

    data.to_csv(output_path, index=False)

    return output_path