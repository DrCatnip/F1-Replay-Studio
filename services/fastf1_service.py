from __future__ import annotations

from typing import Any

import fastf1

from app.constants import CACHE_FOLDER


class FastF1Service:
    """Boundary for all direct FastF1 API access."""

    def __init__(
        self,
        cache_path: str = CACHE_FOLDER
    ) -> None:

        self.cache_path = cache_path
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

        session.load()

        return session

    def extract_drivers(
        self,
        session: Any
    ) -> list[str]:

        drivers: list[str] = []

        for driver in session.laps["Driver"].unique():
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
