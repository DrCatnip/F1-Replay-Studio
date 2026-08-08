from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class PositionData:
    """Array-backed position samples for the hot replay-render path."""

    times_ms: np.ndarray
    x: np.ndarray
    y: np.ndarray

    def position_at(self, timestamp: pd.Timedelta) -> tuple[float, float] | None:
        if not len(self.times_ms):
            return None
        index = int(np.searchsorted(self.times_ms, timestamp.total_seconds() * 1000, side="right") - 1)
        if index < 0:
            return None
        return float(self.x[index]), float(self.y[index])


class ReplayService:
    """Creates replay data structures from loaded FastF1 laps."""

    def position_data_for_lap(
        self,
        lap: Any
    ) -> Any:

        data = lap.get_pos_data()
        if data is None or data.empty or not {"SessionTime", "X", "Y"}.issubset(data.columns):
            return PositionData(np.array([]), np.array([]), np.array([]))
        return PositionData(
            times_ms=data["SessionTime"].dt.total_seconds().to_numpy(dtype=float) * 1000,
            x=data["X"].to_numpy(dtype=float),
            y=data["Y"].to_numpy(dtype=float),
        )

    def time_range(
        self,
        driver_data: Mapping[str, Any]
    ) -> tuple[pd.Timedelta, pd.Timedelta]:

        start_time: pd.Timedelta | None = None
        end_time = pd.Timedelta(seconds=0)

        for pos_data in driver_data.values():
            if not len(pos_data.times_ms):
                continue
            driver_min = pd.Timedelta(milliseconds=float(pos_data.times_ms[0]))
            driver_max = pd.Timedelta(milliseconds=float(pos_data.times_ms[-1]))

            if (
                start_time is None
                or driver_min > start_time
            ):
                start_time = driver_min

            if driver_max > end_time:
                end_time = driver_max

        if start_time is None:
            start_time = pd.Timedelta(seconds=0)

        return (
            start_time,
            end_time
        )
