from __future__ import annotations

from typing import Any, Mapping

import pandas as pd


class ReplayService:
    """Creates replay data structures from loaded FastF1 laps."""

    def position_data_for_lap(
        self,
        lap: Any
    ) -> Any:

        return lap.get_pos_data()

    def time_range(
        self,
        driver_data: Mapping[str, Any]
    ) -> tuple[pd.Timedelta, pd.Timedelta]:

        start_time: pd.Timedelta | None = None
        end_time = pd.Timedelta(seconds=0)

        for pos_data in driver_data.values():
            driver_min = pos_data["SessionTime"].min()
            driver_max = pos_data["SessionTime"].max()

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
