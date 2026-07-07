from __future__ import annotations

import pandas as pd


class PlaybackClock:
    """Looping replay clock used by the pure replay controller."""

    def __init__(
        self,
        tick_milliseconds: int = 100
    ) -> None:

        self.tick_milliseconds = tick_milliseconds
        self.current_time = pd.Timedelta(seconds=0)
        self.start_time = pd.Timedelta(seconds=0)
        self.end_time = pd.Timedelta(seconds=0)
        self.speed = 1.0
        self.playing = True

    def initialize(
        self,
        start_time: pd.Timedelta,
        end_time: pd.Timedelta
    ) -> None:

        self.start_time = start_time
        self.end_time = end_time
        self.current_time = start_time

    def play(self) -> None:
        self.playing = True

    def pause(self) -> None:
        self.playing = False

    def set_speed(
        self,
        speed: float
    ) -> None:

        self.speed = speed

    def seek_progress(
        self,
        progress: float
    ) -> None:

        bounded_progress = max(
            0.0,
            min(
                1.0,
                progress
            )
        )

        duration = self.end_time - self.start_time

        self.current_time = (
            self.start_time
            + duration * bounded_progress
        )

    def advance(self) -> None:
        if not self.playing:
            return

        self.current_time += pd.Timedelta(
            milliseconds=self.tick_milliseconds * self.speed
        )

        if self.current_time > self.end_time:
            self.current_time = self.start_time
