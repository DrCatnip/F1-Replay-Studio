from __future__ import annotations

from typing import Any

from models.session_info import EventInfo, SessionInfo
from services.fastf1_service import FastF1Service


class SessionService:
    """Discovery boundary for seasons, events, and sessions."""

    def __init__(self, fastf1_service: FastF1Service | None = None) -> None:
        self.fastf1_service = fastf1_service or FastF1Service()

    def available_events(self, year: int) -> list[EventInfo]:
        schedule = self.fastf1_service.event_schedule(year)
        events: list[EventInfo] = []
        for _, row in schedule.iterrows():
            name = row.get("EventName")
            if not isinstance(name, str) or not name.strip():
                continue
            event_date = row.get("EventDate")
            events.append(EventInfo(
                year=year,
                name=name,
                round_number=_as_int(row.get("RoundNumber")),
                event_date=event_date.date() if hasattr(event_date, "date") else None,
            ))
        return events

    def available_sessions(self, year: int, event_name: str) -> list[SessionInfo]:
        schedule = self.fastf1_service.event_schedule(year)
        matches = schedule[schedule["EventName"] == event_name]
        if matches.empty:
            return []
        event = matches.iloc[0]
        sessions: list[SessionInfo] = []
        for index in range(1, 6):
            name = event.get(f"Session{index}")
            if not isinstance(name, str) or not name.strip() or name == "nan":
                continue
            sessions.append(SessionInfo(code=_session_code(name), name=name))
        return sessions


def _as_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _session_code(name: str) -> str:
    normalized = name.strip().lower()
    codes = {
        "practice 1": "FP1", "practice 2": "FP2", "practice 3": "FP3",
        "qualifying": "Q", "sprint qualifying": "SQ", "sprint shootout": "SS",
        "sprint": "S", "race": "R",
    }
    return codes.get(normalized, name)
