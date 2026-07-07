from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.constants import CACHE_FOLDER, DEFAULT_EVENT, DEFAULT_SESSION, DEFAULT_YEAR
from core.leaderboard_engine import LeaderboardEngine
from core.replay_controller import ReplayController
from core.telemetry_engine import TelemetryEngine
from core.telemetry import TelemetryData
from services.fastf1_service import FastF1Service
from services.replay_service import ReplayService
from services.telemetry_service import TelemetryService


@dataclass(frozen=True)
class LoadedSession:
    """Application-ready session data for replay, telemetry, and panels."""

    year: int
    event: str
    session_type: str
    drivers: list[str]
    driver_data: dict[str, Any]
    telemetry_data: dict[str, TelemetryData]
    reference_track: Any
    replay_controller: ReplayController
    telemetry_engine: TelemetryEngine
    leaderboard_engine: LeaderboardEngine


class SessionLoader:
    """Loads and adapts FastF1 data into application engines."""

    def __init__(
        self,
        fastf1_service: FastF1Service | None = None,
        replay_service: ReplayService | None = None,
        telemetry_service: TelemetryService | None = None,
        cache_path: str = CACHE_FOLDER,
        year: int = DEFAULT_YEAR,
        event: str = DEFAULT_EVENT,
        session_type: str = DEFAULT_SESSION
    ) -> None:

        self.cache_path = cache_path
        self.year = year
        self.event = event
        self.session_type = session_type
        self.fastf1_service = fastf1_service or FastF1Service(
            cache_path=cache_path
        )
        self.replay_service = replay_service or ReplayService()
        self.telemetry_service = telemetry_service or TelemetryService()

    def load(self) -> LoadedSession:
        session = self.fastf1_service.load_session(
            self.year,
            self.event,
            self.session_type
        )

        drivers = self.fastf1_service.extract_drivers(
            session
        )
        driver_data: dict[str, Any] = {}
        telemetry_data: dict[str, TelemetryData] = {}
        reference_track = None

        for driver in drivers:
            lap = self.fastf1_service.fastest_lap(
                session,
                driver
            )

            if lap is None:
                continue

            pos_data = self.replay_service.position_data_for_lap(
                lap
            )

            driver_data[
                driver
            ] = pos_data

            telemetry_data[
                driver
            ] = self.telemetry_service.telemetry_for_lap(
                lap
            )

            if reference_track is None:
                reference_track = pos_data

        start_time, end_time = self.replay_service.time_range(
            driver_data
        )

        replay_controller = ReplayController(
            driver_data=driver_data,
            start_time=start_time,
            end_time=end_time,
            selected_driver=drivers[0] if drivers else ""
        )

        return LoadedSession(
            year=self.year,
            event=self.event,
            session_type=self.session_type,
            drivers=drivers,
            driver_data=driver_data,
            telemetry_data=telemetry_data,
            reference_track=reference_track,
            replay_controller=replay_controller,
            telemetry_engine=TelemetryEngine(
                telemetry_data
            ),
            leaderboard_engine=LeaderboardEngine(
                drivers
            )
        )
