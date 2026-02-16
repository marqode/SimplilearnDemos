from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Iterable, List

from .parsing import LogEvent


def build_report(events: Iterable[LogEvent]) -> Dict[str, Any]:
    events_list = list(events)

    by_level: Dict[str, int] = {}
    by_component: Dict[str, int] = {}
    error_examples: List[dict] = []

    for e in events_list:
        by_level[e.level] = by_level.get(e.level, 0) + 1
        by_component[e.component] = by_component.get(e.component, 0) + 1

        if e.level == "ERROR" and len(error_examples) < 3:
            error_examples.append(
                {
                    "timestamp": e.timestamp,
                    "component": e.component,
                    "message": e.message,
                    "source": e.source,
                }
            )

    return {
        "summary": {
            "total_events": len(events_list),
            "levels": dict(sorted(by_level.items())),
            "components": dict(sorted(by_component.items())),
        },
        "error_examples": error_examples,
        # Helpful for debugging; keep small.
        "first_event": asdict(events_list[0]) if events_list else None,
    }
