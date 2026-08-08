from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class EventInfo:
    year: int
    name: str
    round_number: int | None = None
    event_date: date | None = None


@dataclass(frozen=True)
class SessionInfo:
    code: str
    name: str
    available: bool = True

