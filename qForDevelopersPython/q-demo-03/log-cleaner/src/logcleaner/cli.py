from __future__ import annotations

import argparse
import json
import sys
from typing import List

from .io_utils import iter_log_lines
from .parsing import parse_line
from .reporting import build_report


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="logcleaner")
    parser.add_argument("paths", nargs="+", help="One or more .log file paths")
    parser.add_argument("--out", help="Write JSON report to a file (default: stdout)")
    args = parser.parse_args(argv)

    events = []
    skipped = 0

    for source, line in iter_log_lines(args.paths):
        evt = parse_line(source, line)
        if evt is None:
            skipped += 1
            continue
        events.append(evt)

    report = build_report(events)
    report["summary"]["skipped_lines"] = skipped

    payload = json.dumps(report, indent=2, sort_keys=True)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(payload + "\n")
    else:
        sys.stdout.write(payload + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
