from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import pandas as pd

from core.interpolation import InterpolationEngine
from core.playback_clock import PlaybackClock


@dataclass(frozen=True)
class DriverState:
    """Position and display state for one driver at a replay timestamp."""

    driver: str
    x: float
    y: float
    selected: bool = False


@dataclass(frozen=True)
class ReplayFrame:
    """Immutable frame consumed by the UI and graphics layer."""

    timestamp: pd.Timedelta
    start_time: pd.Timedelta
    end_time: pd.Timedelta
    speed: float
    selected_driver: str
    drivers: tuple[DriverState, ...]

    @property
    def progress(self) -> float:
        duration = self.end_time - self.start_time

        if duration.total_seconds() <= 0:
            return 0.0

        elapsed = self.timestamp - self.start_time

        return max(
            0.0,
            min(
                1.0,
                elapsed / duration
            )
        )


class ReplayController:
    """Pure replay coordinator with no dependency on PyQt or rendering."""

    def __init__(
        self,
        driver_data: Mapping[str, object],
        start_time: pd.Timedelta,
        end_time: pd.Timedelta,
        selected_driver: str = "",
        tick_milliseconds: int = 33
    ) -> None:

        self.driver_data = dict(driver_data)
        self.selected_driver = selected_driver
        self.interpolation = InterpolationEngine()
        self.clock = PlaybackClock(
            tick_milliseconds=tick_milliseconds
        )
        self.clock.initialize(
            start_time,
            end_time
        )

    def play(self) -> None:
        self.clock.play()

    def pause(self) -> None:
        self.clock.pause()

    def set_speed(
        self,
        speed: float
    ) -> None:

        self.clock.set_speed(
            speed
        )

    def set_selected_driver(
        self,
        driver: str
    ) -> None:

        self.selected_driver = driver

    def seek_progress(
        self,
        progress: float
    ) -> None:

        self.clock.seek_progress(
            progress
        )

    def seek(self, timestamp: pd.Timedelta) -> None:
        duration = self.clock.end_time - self.clock.start_time
        if duration.total_seconds() > 0:
            self.seek_progress((timestamp - self.clock.start_time) / duration)

    def advance(self) -> None:
        self.clock.advance()

    def get_current_frame(self) -> ReplayFrame:
        states: list[DriverState] = []

        for driver, data in self.driver_data.items():
            position = self.interpolation.position_at(
                data,
                self.clock.current_time
            )

            if position is None:
                continue

            x, y = position

            states.append(
                DriverState(
                    driver=driver,
                    x=x,
                    y=y,
                    selected=driver == self.selected_driver
                )
            )

        return ReplayFrame(
            timestamp=self.clock.current_time,
            start_time=self.clock.start_time,
            end_time=self.clock.end_time,
            speed=self.clock.speed,
            selected_driver=self.selected_driver,
            drivers=tuple(states)
        )
