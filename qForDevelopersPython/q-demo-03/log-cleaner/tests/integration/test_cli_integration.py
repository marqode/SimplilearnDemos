import json
import subprocess
import sys
from pathlib import Path


def test_cli_outputs_valid_json(tmp_path: Path):
    out_file = tmp_path / "report.json"

    # Run the installed console script via python -m to be robust in editable installs
    cmd = [
        sys.executable,
        "-m",
        "logcleaner.cli",
        "sample_data/app1.log",
        "sample_data/app2.log",
        "--out",
        str(out_file),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr

    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert "summary" in data
    assert data["summary"]["total_events"] >= 1
    assert "levels" in data["summary"]
