import pandas as pd

from radlabpy.cli import main


def test_cli_help(capsys):
    exit_code = main(["--help"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "usage:" in captured.out
    assert "geiger" in captured.out
    assert "spectrum" in captured.out
    assert "calibration" in captured.out
    assert "hep" in captured.out
    assert "detector" in captured.out


def test_cli_version(capsys):
    exit_code = main(["--version"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "radlabpy" in captured.out


def test_cli_geiger_with_temporary_csv(tmp_path, capsys):
    csv_path = tmp_path / "geiger.csv"

    data = pd.DataFrame(
        {
            "counts": [20, 22, 19, 25, 24],
        }
    )
    data.to_csv(csv_path, index=False)

    exit_code = main(["geiger", str(csv_path), "--counts-col", "counts"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Geiger counting summary" in captured.out
    assert "Mean" in captured.out
    assert "Standard deviation" in captured.out
    assert "Minimum" in captured.out
    assert "Maximum" in captured.out


def test_cli_spectrum_with_temporary_csv(tmp_path, capsys):
    csv_path = tmp_path / "spectrum.csv"

    data = pd.DataFrame(
        {
            "channel": [1, 2, 3, 4, 5],
            "counts": [5, 12, 30, 14, 6],
        }
    )
    data.to_csv(csv_path, index=False)

    exit_code = main(
        [
            "spectrum",
            str(csv_path),
            "--channel-col",
            "channel",
            "--counts-col",
            "counts",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Spectrum summary" in captured.out
    assert "Total counts" in captured.out
    assert "Peak channel" in captured.out


def test_cli_spectrum_with_gaussian_fit(tmp_path, capsys):
    csv_path = tmp_path / "spectrum_fit.csv"

    data = pd.DataFrame(
        {
            "channel": [1, 2, 3, 4, 5, 6, 7],
            "counts": [10, 18, 45, 80, 46, 20, 11],
        }
    )
    data.to_csv(csv_path, index=False)

    exit_code = main(["spectrum", str(csv_path), "--fit-gaussian"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Gaussian fit" in captured.out
    assert "Amplitude" in captured.out
    assert "Mean" in captured.out
    assert "Sigma" in captured.out
    assert "FWHM" in captured.out


def test_cli_calibration_with_temporary_csv(tmp_path, capsys):
    csv_path = tmp_path / "calibration.csv"

    data = pd.DataFrame(
        {
            "channel": [100, 200, 300, 400],
            "energy": [50, 100, 150, 200],
        }
    )
    data.to_csv(csv_path, index=False)

    exit_code = main(
        [
            "calibration",
            str(csv_path),
            "--channel-col",
            "channel",
            "--energy-col",
            "energy",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Energy calibration" in captured.out
    assert "Slope" in captured.out
    assert "Intercept" in captured.out
    assert "R squared" in captured.out


def test_cli_hep_with_temporary_csv(tmp_path, capsys):
    csv_path = tmp_path / "hep_events.csv"

    data = pd.DataFrame(
        {
            "E": [5.0, 10.0],
            "px": [3.0, 6.0],
            "py": [0.0, 0.0],
            "pz": [0.0, 0.0],
        }
    )
    data.to_csv(csv_path, index=False)

    exit_code = main(["hep", str(csv_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "HEP invariant mass summary" in captured.out
    assert "Number of events" in captured.out
    assert "Mean mass" in captured.out


def test_cli_detector_with_counting_columns(tmp_path, capsys):
    csv_path = tmp_path / "detector.csv"

    data = pd.DataFrame(
        {
            "counts": [100, 120, 140],
            "time": [10, 10, 10],
        }
    )
    data.to_csv(csv_path, index=False)

    exit_code = main(["detector", str(csv_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Detector summary" in captured.out
    assert "Event rate" in captured.out
    assert "Mean rate" in captured.out


def test_cli_missing_file_error(capsys):
    exit_code = main(["geiger", "not_existing_file.csv"])
    captured = capsys.readouterr()

    assert exit_code != 0
    assert "Error" in captured.out
    assert "not_existing_file.csv" in captured.out