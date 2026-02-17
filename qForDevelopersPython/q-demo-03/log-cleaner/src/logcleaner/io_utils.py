from __future__ import annotations

from pathlib import Path
from typing import Iterable


def iter_log_lines(paths: Iterable[str]) -> Iterable[tuple[str, str]]:
    """
    Yield (source_path, raw_line) for each line in each file.

    - Skips blank lines
    - Skips comment lines starting with '#'
    """
    for path in _expand_paths(paths):
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                yield (str(path), line.rstrip("\n"))

def _expand_paths(paths: Iterable[str]) -> list[Path]:
    expanded: list[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            expanded.extend(sorted(path.glob("*.log")))
        else:
            expanded.append(path)
    return expanded

