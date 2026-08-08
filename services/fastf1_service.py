from __future__ import annotations

from typing import Any
from pathlib import Path

import fastf1

from app.constants import CACHE_FOLDER


class FastF1Service:
    """Boundary for all direct FastF1 API access."""

    def __init__(
        self,
        cache_path: str = CACHE_FOLDER
    ) -> None:

        self.cache_path = str(Path(cache_path).resolve())
        Path(self.cache_path).mkdir(parents=True, exist_ok=True)
        fastf1.Cache.enable_cache(
            self.cache_path
        )

    def load_session(
        self,
        year: int,
        event: str,
        session_type: str
    ) -> Any:

        session = fastf1.get_session(
            year,
            event,
            session_type
        )

        # Telemetry is requested because it is the core replay input. FastF1
        # still returns useful metadata/results when a particular session has
        # no telemetry available.
        session.load(telemetry=True, weather=False, messages=True)

        return session

    def event_schedule(self, year: int) -> Any:
        """Return the provider schedule without exposing FastF1 to the UI."""
        return fastf1.get_event_schedule(year, include_testing=False)

    def extract_drivers(
        self,
        session: Any
    ) -> list[str]:

        drivers: list[str] = []

        if getattr(session, "laps", None) is None or "Driver" not in session.laps:
            return drivers

        for driver in session.laps["Driver"].dropna().unique():
            if isinstance(driver, str):
                drivers.append(
                    driver
                )

        return drivers

    def fastest_lap(
        self,
        session: Any,
        driver: str
    ) -> Any | None:

        try:
            return (
                session.laps
                .pick_drivers(driver)
                .pick_fastest()
            )
        except Exception:
            return None

    def leaderboard_rows(self, session: Any) -> list[dict[str, object]]:
        """Adapt official result metadata where it is available."""
        results = getattr(session, "results", None)
        if results is None or results.empty:
            return []
        rows: list[dict[str, object]] = []
        for _, result in results.iterrows():
            driver = result.get("Abbreviation")
            if not isinstance(driver, str):
                continue
            rows.append({
                "driver": driver,
                "team": result.get("TeamName", "—"),
                "position": result.get("Position", "—"),
                "gap": result.get("Time", "—"),
                "lap": result.get("NumberOfLaps", "—"),
                "tyre": "—",
            })
        return rows
