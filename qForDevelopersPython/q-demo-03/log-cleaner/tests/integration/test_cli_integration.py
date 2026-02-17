import json
import subprocess
import sys
from pathlib import Path

def test_cli_writes_valid_report_json(tmp_path: Path):
    """
    Integration-style test:
    - Runs the CLI as a subprocess (closest to real usage)
    - Uses absolute paths to sample data (no cwd/path guessing)
    - Produces helpful diagnostics if anything goes wrong
    """
    repo_root = Path(__file__).resolve().parents[2]  # log-cleaner/
    sample_dir = repo_root / "sample-data"
    app1 = sample_dir / "app1.log"
    app2 = sample_dir / "app2.log"

    # Preflight checks make failures obvious (and Q-friendly)
    assert app1.exists(), f"Missing sample file: {app1}"
    assert app2.exists(), f"Missing sample file: {app2}"

    out_file = tmp_path / "report.json"

    # Run the CLI module using the venv Python.
    # cwd is repo_root so relative imports/resources behave like normal local runs.
    cmd = [
        sys.executable,
        "-m",
        "logcleaner.cli",
        str(app1),
        str(app2),
        "--out",
        str(out_file),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_root)

    assert result.returncode == 0, (
        "CLI returned non-zero exit code.\n"
        f"cmd: {' '.join(cmd)}\n"
        f"cwd: {repo_root}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}\n"
    )

    assert out_file.exists(), (
        "CLI succeeded but did not create the output file.\n"
        f"Expected: {out_file}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}\n"
    )

    raw = out_file.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise AssertionError(
            "Output file is not valid JSON.\n"
            f"File: {out_file}\n"
            f"Error: {e}\n"
            f"First 400 chars:\n{raw[:400]}\n"
        )

    # Schema-level assertions: stable, not overly specific.
    assert isinstance(data, dict), "Report JSON should be an object at the top level."
    assert "summary" in data, "Report must contain a top-level 'summary' key."
    assert isinstance(data["summary"], dict), "'summary' must be an object."

    # These keys are intentionally broad: good for confidence, low brittleness.
    assert "total_events" in data["summary"], "summary must include 'total_events'."
    assert isinstance(data["summary"]["total_events"], int), "'total_events' must be an int."
    assert data["summary"]["total_events"] >= 1, "Expected at least 1 parsed event from sample logs."

    assert "levels" in data["summary"], "summary must include 'levels' breakdown."
    assert isinstance(data["summary"]["levels"], dict), "'levels' must be an object/dict."
    assert len(data["summary"]["levels"]) >= 1, "Expected at least one log level in breakdown."