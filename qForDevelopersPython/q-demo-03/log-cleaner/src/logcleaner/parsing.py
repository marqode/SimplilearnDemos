from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LogEvent:
    timestamp: str
    level: str
    component: str
    message: str
    source: str


VALID_LEVELS = {"DEBUG", "INFO", "WARN", "ERROR"}


def parse_line(source: str, line: str) -> Optional[LogEvent]:
    """
    Parse one log line.

    Expected format:
      <timestamp> <level> <component> <message...>

    Returns None for lines that don't match expectations.
    """
    parts = line.split(" ", 3)
    if len(parts) < 4:
        return None

    timestamp, level, component, message = parts[0], parts[1], parts[2], parts[3]
    level = level.upper()
    if level not in VALID_LEVELS:
        return None

    component = component.strip()
    message = message.strip()

    return LogEvent(
        timestamp=timestamp,
        level=level,
        component=component,
        message=message,
        source=source,
    )
