from __future__ import annotations

import numpy as np
import pandas as pd


class TelemetryData:

    def __init__(self, lap):

        self.car_data = lap.get_car_data()
        self.times_ms = (
            self.car_data["SessionTime"].dt.total_seconds().to_numpy(dtype=float) * 1000
            if "SessionTime" in self.car_data and not self.car_data.empty else np.array([])
        )

    def get_sample(self, frame):

        if frame >= len(self.car_data):
            frame = len(self.car_data) - 1

        return self._sample_row(self.car_data.iloc[frame])

    def get_sample_at_time(
        self,
        timestamp: pd.Timedelta
    ) -> dict[str, object] | None:
        if len(self.car_data) == 0:
            return None

        if not len(self.times_ms):
            return self.get_sample(0)
        index = max(0, int(np.searchsorted(self.times_ms, timestamp.total_seconds() * 1000, side="right") - 1))
        return self._sample_row(self.car_data.iloc[index])

    @staticmethod
    def _sample_row(row):
        return {
            "speed": row.get("Speed"), "gear": row.get("nGear"),
            "throttle": row.get("Throttle"), "brake": row.get("Brake"),
            "rpm": row.get("RPM"), "drs": row.get("DRS", "—"),
        }
