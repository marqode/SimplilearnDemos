from __future__ import annotations

from pathlib import Path
from typing import Iterable


def iter_log_lines(paths: Iterable[str]) -> Iterable[tuple[str, str]]:
    """
    Yield (source_path, raw_line) for each line in each file.

    - Skips blank lines
    - Skips comment lines starting with '#'
    """
    for p in paths:
        path = Path(p)
        with path.open("r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip("\n")
                if not line.strip():
                    continue
                if line.lstrip().startswith("#"):
                    continue
                yield (str(path), line)
